# -*- coding: utf-8 -*-
import re
import sys
import time
import requests

from os import getcwd
from redis import Redis
from threading import Thread
from queue import Queue, Empty
from functools import partial

from toolkit.monitors import Service
from toolkit import load_function, load_module
from toolkit.managers import Blocker, ExceptContext

from .import proxy_site_spider
from .utils import exception_wrapper
from . import settings

__version__ = "0.2.0"


class ProxyFactory(Service):
    name = "proxy_factory"
    current_dir = getcwd()
    default_settings = settings
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }

    def __init__(self):
        """
            初始化logger, redis_conn
        """
        super(ProxyFactory, self).__init__()
        sys.path.insert(0, self.current_dir)
        self.proxies_check_in_queue = Queue()
        self.proxies_check_out_queue = Queue()
        self.load_site(proxy_site_spider)
        self.load_site(self.args.spider_module)
        self.redis_conn = Redis(self.settings.get("REDIS_HOST"), self.settings.get_int("REDIS_PORT"))
        if self.args.check_method:
            self.check_method = partial(load_function(self.args.check_method), self)

    def load_site(self, module_str):
        if module_str:
            if isinstance(module_str, str):
                mod = load_module(module_str)
            else:
                mod = module_str
            for key, func in vars(mod).items():
                if key.startswith("fetch"):
                    self.__dict__[key] = partial(exception_wrapper(func), self)

    def check_method(self, proxy):
        resp = requests.get(
            "http://www.whatismyip.com.tw/", headers=self.headers, timeout=10,
            proxies={"http": "http://%s" % proxy})
        ip, real_ip = re.search(r'"ip": "(.*?)"[\s\S]+"ip-real": "(.*?)",', resp.text).groups()
        self.logger.debug("IP: %s. Real IP: %s. Proxy: %s" % (ip, real_ip, proxy))
        return resp.status_code < 300 and not real_ip

    def check(self, proxy, good):
        """
            检查代理是否可用
        """
        with ExceptContext(errback=lambda *args: True):
            if self.check_method(proxy):
                good.append(proxy)

    def check_proxies(self):
        """
        对待检查队列中的代理进行检查
        :return:
        """
        self.logger.debug("Start check thread. ")
        while self.alive:
            with ExceptContext(errback=self.log_err):
                try:
                    proxies = self.proxies_check_in_queue.get_nowait()
                except Empty:
                    proxies = None
                if proxies:
                    self.logger.debug("Got %s proxies to check. " % len(proxies))
                    proxies = [proxy.decode() if isinstance(proxy, bytes) else proxy for proxy in proxies]
                    good = list()
                    for i in range(0, len(proxies), 150):
                        # 分批检查
                        thread_list = []
                        for proxy in proxies[i: i+150]:
                            th = Thread(target=self.check, args=(proxy, good))
                            th.setDaemon(True)
                            th.start()
                            thread_list.append(th)
                        start_time = time.time()
                        while [thread for thread in thread_list if thread.is_alive()] and start_time + 60 > time.time():
                            time.sleep(1)

                    self.logger.debug("%s proxies is good. " % (len(good)))
                    self.proxies_check_out_queue.put(dict((proxy, proxy in good) for proxy in proxies))
                else:
                    time.sleep(1)
            time.sleep(1)
        self.logger.debug("Stop check thread. ")

    def bad_source(self):
        """
        每隔指定时间间隔将无效代理放到待检查队列进行检查
        :return:
        """
        self.logger.debug("Start bad source thread. ")
        while self.alive:
            with Blocker(self.settings.get_int("BAD_CHECK_INTERVAL", 60 * 5),
                         self, notify=lambda instance: not instance.alive) as blocker:
                if blocker.is_notified:
                    continue
                with ExceptContext(errback=self.log_err):
                    proxies = self.redis_conn.hgetall("bad_proxies")
                    if proxies:
                        self.logger.debug("Bad proxy count is : %s, ready to check. " % len(proxies))
                        for proxy, times in proxies.items():
                            if int(times) > self.settings.get_int("FAILED_TIMES", 5):
                                self.redis_conn.hdel("bad_proxies", proxy)
                                self.logger.debug("Abandon %s of failed for %s times. " % (proxy, times))
                        self.proxies_check_in_queue.put(proxies.keys())
        self.logger.debug("Stop bad source thread. ")

    def good_source(self):
        """
        每隔指定时间间隔将有效代理放到待检查队列进行检查
        :return:
        """
        self.logger.debug("Start good source thread. ")
        while self.alive:
            with Blocker(self.settings.get_int("GOOD_CHECK_INTERVAL", 60 * 5),
                         self, notify=lambda instance: not instance.alive) as blocker:
                if blocker.is_notified:
                    continue
                with ExceptContext(errback=self.log_err):
                    proxies = self.redis_conn.smembers("good_proxies")
                    if proxies:
                        self.logger.debug("Good proxy count is : %s, ready to check. " % len(proxies))
                        self.proxies_check_in_queue.put(proxies)
        self.logger.debug("Stop good source thread. ")

    def reset_proxies(self):
        """
        分发有效代理和无效代理
        :return:
        """
        self.logger.debug("Start resets thread. ")
        while self.alive:
            with ExceptContext(errback=self.log_err):
                try:
                    proxies = self.proxies_check_out_queue.get_nowait()
                except Empty:
                    proxies = None
                if proxies:
                    self.logger.debug("Got %s proxies to reset. " % len(proxies))
                    for proxy, good in proxies.items():
                        if good:
                            self.redis_conn.sadd("good_proxies", proxy)
                            self.redis_conn.hdel("bad_proxies", proxy)
                        else:
                            self.redis_conn.hincrby("bad_proxies", proxy)
                            self.redis_conn.srem("good_proxies", proxy)
                else:
                    time.sleep(1)
            time.sleep(1)
        self.logger.debug("Stop resets thread. ")

    def gen_thread(self, target, name=None, args=(), kwargs=None):
        thread = Thread(target=target, name=name, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
        self.children.append(thread)

    def start(self):
        self.logger.debug("Start proxy factory. ")
        self.gen_thread(self.check_proxies)
        self.gen_thread(self.bad_source)
        self.gen_thread(self.good_source)
        self.gen_thread(self.reset_proxies)
        is_started = False
        while self.alive or [thread for thread in self.children if thread.is_alive()]:
            with Blocker(self.settings.get_int("FETCH_INTERVAL", 10 * 60),
                         self, notify=lambda instance: not instance.alive, immediately=not is_started) as blocker:
                if blocker.is_notified:
                    continue
                with ExceptContext(errback=self.log_err):
                    if self.alive:
                        self.logger.debug("Start to fetch proxies. ")
                        proxies = self.fetch_all()
                        self.logger.debug("%s proxies found. " % len(proxies))
                        self.proxies_check_in_queue.put(proxies)
            is_started = True
        self.logger.debug("Stop proxy factory. ")

    def fetch_all(self):
        """
            获取全部网站代理，内部调用各网站代理获取函数
        """
        proxies = set()
        for key, value in self.__dict__.items():
            if key.startswith("fetch"):
                proxies.update(value())
        return proxies

    def enrich_parser_arguments(self):
        self.parser.add_argument("-cm", "--check-method", help="proivde a check method to check proxies. eg:module.func")
        self.parser.add_argument("-sm", "--spider-module",
                            help="proivde a module contains proxy site spider methods. eg:module1.module2")
        return super(ProxyFactory, self).enrich_parser_arguments()


def main():
    ProxyFactory().start()


if __name__ == '__main__':
    main()
