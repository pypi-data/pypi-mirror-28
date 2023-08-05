import json
import socket
import traceback
from concurrent import futures
from loader.function import load
import geoip2.database

import time
from urllib.parse import urlparse

import websocket

from netboy.chrome.interface import ChromeInterface

# import falsy
#
#
# class ChromeShortException(Exception):
#     pass
#
#
# class ChromeEmptyException(Exception):
#     pass
#
#
# class ChromeECMAScriptException(Exception):
#     pass
#
#
# import asyncio as aio
#
#
# class ChromeTargetException(Exception):
#     pass
from netboy.util.aop_wrapper import pre_process, post_process
from netboy.util.grouper import grouper_it
from netboy.util.makeup import Makeup
from netboy.util.payload import Payload
from selenium import webdriver


class ChromeBoy:
    def __init__(self, **kwargs):
        self.chrome_bin = kwargs.get('chrome', '/opt/google/chrome-beta/chrome')
        self.window_size = kwargs.get('window_size', '1200x600')
        self.load_timeout = kwargs.get('load_timeout', 10)
        self.screenshot = kwargs.get('screenshot')
        options = webdriver.ChromeOptions()
        options.binary_location = self.chrome_bin
        options.add_argument('headless')

        options.add_argument('window-size=' + self.window_size)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.set_page_load_timeout(10)

    # def run(self, payload):
    #     self.driver.get('')
    def run(self, payload):
        url = payload.get('url')
        load_timeout = payload.get('load_timeout')
        if load_timeout:
            self.driver.set_page_load_timeout(10)
        implicit_wait = payload.get('implicit_wait', 10)
        start = time.time()
        self.driver.get(url)
        self.driver.implicitly_wait(implicit_wait)

        end = time.time()
        screenshot = payload.get('screenshot') or self.screenshot
        resp = {
            'url': url,
            'current_url': self.driver.current_url,
            'source': self.driver.page_source,
            'title': self.driver.title,
            'spider': 'selenium_chrome',
            'state': 'normal',
            "http_code": 200,
            'time': '%s' % (end - start)
        }
        if screenshot:
            resp['screenshot'] = self.driver.get_screenshot_as_base64()
        return resp

    def get(self, url, **kwargs):
        kwargs['url'] = url
        r = self.run(**kwargs)
        return r

    def close(self):
        self.driver.close()


class ConcurrentBoy:
    def run(self, payload):
        data = payload.get('data')
        info = payload.get('info')
        mode = info.get('mode', 'normal')
        if 'multi' in mode or 'process' in mode or 'thread' in mode:
            return self._run_multi(data, info, mode)
        return self._run_simple(data, info)

    def run1(self, payload):
        payload = pre_process(payload)
        url = payload.get('url')
        # mode = payload.get('mode', 'quick')
        if not url:
            return None
        a = ChromeBoy()
        r = a.run(payload)
        r = post_process(payload, r)
        a.close()
        return r

    def _run_multi(self, data, info, mode='process'):
        results = []
        for chunked_data in grouper_it(data, info.get('chunk_size', 10)):
            result = self._run(chunked_data, info, mode)
            results.extend(result)
        return results

    def _run_simple(self, data, info):
        results = []
        for chunked_data in grouper_it(data, 4):
            info['max_workers'] = 2
            result = self._run(chunked_data, info, 'thread')
            results.extend(result)
        return results

    def _run(self, data, info, mode='process'):
        Executor = futures.ThreadPoolExecutor if 'thread' in mode else futures.ProcessPoolExecutor
        results = []
        with Executor(max_workers=info.get("max_workers")) as executor:
            future_to_url = {}
            for i, payload in enumerate(data):
                d = {'url': payload} if type(payload) is str else payload
                # d.update(info)
                Payload.update(d, info, ['max_workers, chunk_size'])
                future_to_url[executor.submit(self.run1, d)] = d

            for future in futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                    traceback.print_tb(exc.__traceback__)
                else:
                    results.append(data)
        return results

    def view(self, results, filters):
        scene = []
        for result in results:
            updated = {key: result.get(key) for key in filters}
            scene.append(updated)
        return scene


if __name__ == '__main__':
    boy = ChromeBoy()
    r, c = boy.new_page('http://www.baidu.com', cookies=True, screenshot=True)
    print(r.keys())
    # print(r['title'])
    # print(r['time'])
    # print(r['cookies'])
    # boy.screenshot(c)
    # boy.close()





    # a = ConcurrentBoy()
    # r = a.run({
    #     'data': [
    #         'http://www.baidu.com',
    #         {'url': 'http://www.douban.com',
    #          'useragent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
    #          },
    #         # 'http://www.facebook.com',
    #     ],
    #     'info': {'chunk_size': 2, 'max_worker': 2,
    #              'cookies': True,
    #              'screenshot': True,
    #              # 'xhr': True,
    #              'mode': 'quick'
    #              }
    # })
    # print(json.dumps(a.view(r, ['ip', 'hostname', 'title', 'location', 'time', 'url', 'referer', 'URL', 'mode']),
    #                  indent=2, ensure_ascii=False))
    #
    boy = ChromeBoy()
    r = boy.get('http://www.baidu.com')
    # r = boy.get('https://www.seebug.org/rss/new/')
    print(r)
    #
