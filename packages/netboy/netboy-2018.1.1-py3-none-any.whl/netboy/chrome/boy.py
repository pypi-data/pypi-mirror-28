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


class ChromeBoy:
    def __init__(self, **kwargs):
        self._host = kwargs.get('host', '127.0.0.1')
        self._port = kwargs.get('port', 9222)
        self._dev_id = kwargs.get('dev_id', 'invalid')
        if isinstance(self._port, int):
            self._url = '%s:%d' % (self._host, self._port)
        else:
            self._url = '%s:%s' % (self._host, self._port)
        self._socket_timeout = kwargs.get('sockettimeout', 20)
        self._browser_url = 'ws://' + self._url + '/devtools/browser/' + self._dev_id
        self._id = 0
        self._user_agent = kwargs.get('useragent')
        self._http_header = kwargs.get('httpheader')
        self._cookies = kwargs.get('cookies')
        self._load_timeout = kwargs.get('loadtimeout', 15)
        self._auto_connect = kwargs.get('auto_connect', True)
        self._tabs = {}
        self._targets = []

    def screenshot(self, c=None, shot_quality=40, shot_format='jpeg'):
        if c is None:
            c = self.c
        try:
            doc_id = c.DOM.getDocument()['result']['root']['nodeId']
            body_id = c.DOM.querySelector(selector="body", nodeId=doc_id)['result']['nodeId']
            box = c.DOM.getBoxModel(nodeId=body_id)['result']['model']
            width, height = box['width'], box['height']
            c.Emulation.setVisibleSize(width=width, height=height)
            c.Emulation.forceViewport(x=0, y=0, scale=1)
            if height > 2000:
                time.sleep((height // 1000) * 0.05)
            screen = c.Page.captureScreenshot(format=shot_format, quality=shot_quality, fromSurface=False)["result"][
                "data"]
        except Exception as e:
            print(e, type(e))
            print('error when shot')
        return screen

    def cookies(self, c=None):
        if c is None:
            c = self.c
        cookies = c.Network.getCookies()['result']['cookies']
        # print('cookies', cookies)
        return cookies

    def useragent(self, c=None, useragent=None):
        if useragent is None:
            return
        if c is None:
            c = self.c
        c.Network.setUserAgentOverride(userAgent=useragent)

    def httpheader(self, c=None, headers=None):
        if c is None:
            c = self.c
        c.Network.setExtraHTTPHeaders(headers=headers)

    def new_page(self, **kwargs):
        try:
            host = kwargs.get('host') or self._host
            port = kwargs.get('port') or self._port
            dev_id = kwargs.get('dev_id')
            if host or port or self._dev_id == 'invalid':
                self._host = host or self._host
                self._port = port or self._port
                self._dev_id = dev_id or self._dev_id
                self._url = '%s:%s' % (self._host, self._port)
                self._browser_url = 'ws://' + self._url + '/devtools/browser/' + self._dev_id
            url = kwargs.get('url')
            if not url.startswith('http'):
                url = 'http://' + url
            start = time.time()
            c, bsock = self.chrome()
            if c is None or bsock is None:
                return {'url': url, 'state': 'error', 'mode': kwargs.get('mode'), 'spider': 'chrome',
                        'error_code': -2, 'error_desc': 'chrome socket or browser socket is None'}, None, None
            self._targets.append(c.target_id)
            c.Network.enable()
            c.Page.enable()
            self.useragent(c, self._user_agent)
            c.Page.navigate(url=url)
            c.wait_event("Page.frameStoppedLoading", timeout=30)
            end = time.time()
            ss = '''
                JSON.stringify({
                    "title": document.title,
                    "window_location": {
                        "href": window.location.href,
                        "origin": window.location.origin,
                        "host": window.location.host,
                        "hostname": window.location.hostname,
                        "pathname": window.location.pathname,
                        "port": window.location.port,
                        "protocol": window.location.protocol,
                        "search": window.location.search,
                    },
                    "charset": document.charset,
                    "text": document.body.innerText,
                    "body": document.body.outerHTML,
                    "head": document.head.outerHTML,
                    "last_modified": document.lastModified,
                    "URL": document.URL,
                    "links": Array.prototype.map.call(document.links,function(link){return link.href})
                    .filter(function(text){ return !text.startsWith('javascript') && text.length > 0;;}),
                    "links2": Array.prototype.map.call(document.querySelectorAll("link"),function(link){return link.href || link.innerHTML })
                    .filter(function(text){ return !text.startsWith('javascript') && text.length > 0;;}),
                    "scripts": Array.prototype.map.call(document.scripts,function(script){return script.src})
                    .filter(function(text){ return !text.startsWith('javascript') && text.length > 0;;}),
                    "images": Array.prototype.map.call(document.images,function(img){return img.src})
                    .filter(function(text){ return !text.startsWith('javascript') && text.length > 0;;}),
                    "url": "%s",
                    "time": %f,
                    "http_code": 200
                });
                ''' % (url, end - start)
            r = c.Runtime.evaluate(expression=ss)
            c.wait_event("Network.responseReceived", timeout=15)
            result_except_flag = False
            result = None
            try:
                result = r['result']['result']
            except Exception as e:
                print(e, type(e), 'error when getting result from response: {}'.format(url))
                result_except_flag = True
            if result is None or not result.get('value') or result_except_flag:
                ss = '''
                JSON.stringify({
                    "title": document.title,
                    "window_location": {
                        "href": window.location.href,
                        "origin": window.location.origin,
                        "host": window.location.host,
                        "hostname": window.location.hostname,
                        "pathname": window.location.pathname,
                        "port": window.location.port,
                        "protocol": window.location.protocol,
                        "search": window.location.search,
                    },
                    "charset": document.charset,
                    "text": document.body.innerText,
                    "body": document.body.outerHTML,
                    "head": document.head.outerHTML,
                    "last_modified": document.lastModified,
                    "URL": document.URL,
                    "links": [],
                    "links2": [],
                    "scripts": [],
                    "images": [],
                    "url": "%s",
                    "time": %f,
                    "http_code": 200
                });
                ''' % (url, end - start)
                r = c.Runtime.evaluate(expression=ss)
                c.wait_event("Network.responseReceived", timeout=15)
                try:
                    result = r['result']['result']
                except Exception as e:
                    error_desc = 'error when getting result from response again: {}'.format(url)
                    print(e, type(e), error_desc)
                    r = {'url': url, 'state': 'error', 'mode': kwargs.get('mode'), 'spider': 'chrome',
                         'error_code': -1, 'error_desc': error_desc}
                    self._tabs[c] = r

                    return r, c, bsock
            try:
                r = result['value']
                r = json.loads(r)

            except Exception as e:

                error_desc = 'error when get value: {}'.format(url)
                print(e, type(e), error_desc)
                r = {'url': url, 'state': 'error', 'mode': kwargs.get('mode'), 'spider': 'chrome',
                     'error_code': -1, 'error_desc': error_desc}
                self._tabs[c] = r

                return r, c, bsock
            self.update_effect(r)
            if kwargs.get('screenshot'):
                r['screenshot'] = self.screenshot(c, shot_quality=kwargs.get('shot_quality', 40),
                                                  shot_format=kwargs.get('shot_format', 'jpeg'))
            if kwargs.get('cookies'):
                r['cookies'] = self.cookies(c)
            r['spider'] = 'chrome'
            r['state'] = 'normal2' if result_except_flag else 'normal'
            r['mode'] = kwargs.get('mode')
            geoip = kwargs.get('geoip')
            ip = r.get('ip')
            try:
                if geoip and ip and len(ip) > 0:
                    reader = geoip2.database.Reader(geoip)
                    response = reader.city(ip)
                    r['geoip'] = response.raw
            except Exception as e:
                print('geoip failed', ip)
                r['geoip'] = None
            self._tabs[c] = r
            pycurl = kwargs.get('pycurl_compatible')
            if pycurl:
                head, body = r.pop('head'), r.pop('body')
                c_time = r.pop('time')
                r['data'] = head + body
                r['total_time'] = c_time
        except Exception as e:
            r = {'url': url, 'state': 'error', 'mode': kwargs.get('mode'), 'spider': 'chrome',
                 'error_code': -2, 'error_desc': 'error when run chrome new page'}
            return r, None, None

        return r, c, bsock

    def quick_page(self, **kwargs):
        r, c, bsock = self.new_page(**kwargs)

        if c:
            self.safe_close(c)
        # 关闭browser的socket
        if bsock:
            bsock.close()
        return r

    def safe_close(self, c):
        # 关闭当前c的tab
        c.close_target()
        # 关闭c的socket
        c.close()
        # recheck close state
        self.close()

    def run(self, payload):
        return self.quick_page(**payload)

    def get(self, url, **kwargs):
        kwargs['url'] = url
        r = self.quick_page(**kwargs)
        return r

    def update_effect(self, r):
        try:
            effect = r['URL'] if r['URL'].startswith('http') else r['url']
            hostname = urlparse(effect).hostname if effect else None
            r['effective_url'] = effect
            r['hostname'] = hostname
            r['ip'] = socket.gethostbyname(hostname) if hostname else None
        except Exception as e:
            print(e, type(e))
            print('error when effect')

    def chrome(self):
        browser_socket = None
        try:
            browser_socket = websocket.create_connection(self._browser_url,
                                                         timeout=self._socket_timeout)
        except Exception as e:
            print(e, type(e), 'error when create socket for chrome()')
            if browser_socket:
                browser_socket.close()

            time.sleep(0.5)
            try:
                browser_socket = websocket.create_connection(self._browser_url,
                                                             timeout=self._socket_timeout)
            except Exception as e:
                print(e, type(e), 'error when create socket for chrome() again')
                return None, None

        try:
            ci = ChromeInterface(browser_socket, self._host, self._port)
        except Exception as e:
            print(e, type(e), 'error when get chrome interface')
            try:
                time.sleep(1)
                ci = ChromeInterface(browser_socket, self._host, self._port)
            except Exception as e:
                print(e, type(e), 'error when get chrome interface again')
                if browser_socket:
                    browser_socket.close()
                return None, None
        return ci, browser_socket

    def close(self):
        # sock = websocket.create_connection(self._browser_url,  # + '/9d220c5c-7eba-4927-a95c-dfd56c689779',
        #                                    timeout=self._socket_timeout)
        # c = ChromeInterface(self.browser, self._host, self._port)
        c, bsock = self.chrome()
        if c is None:
            return
        for target_id in self._targets:
            result = c.close_target(target_id)
        # 关闭c的tab页面
        c.close_target(c.target_id)
        # 关闭c的page sock
        c.close()
        bsock.close()


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
        dev_id = payload.get('dev_id')
        if not dev_id or dev_id == 'invalid':
            raise Exception('dev id invalid')
        a = ChromeBoy(
            # **payload
            host=payload.get('host', 'localhost'),
            port=payload.get('port', 9222),
            useragent=payload.get('useragent'),
            sockettimeout=payload.get('sockettimeout'),
            httpheader=payload.get('httpheader'),
            dev_id=dev_id
        )
        # if mode == 'quick':
        payload['mode'] = 'normal'
        r = a.quick_page(
            **payload
            # url=payload.get('url'),
            # cookies=payload.get('cookies'),
            # screenshot=payload.get('screenshot'),
            # geoip=payload.get('geoip'),
            # mode='normal'
        )
        # else:
        # r, c = a.new_page(url=payload.get('url'),
        #                   cookies=payload.get('cookies'),
        #                   screenshot=payload.get('screenshot'),
        #                   mode='normal'
        #                   )
        a.close()
        r = post_process(payload, r)
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
            # for payload in chunked_data:
            #     d = {'url': payload} if type(payload) is str else payload
            #     Payload.update(d, info, ['max_workers, chunk_size', 'host', 'port'])
            #     result = self.run1(d)
            #     results.append(result)
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
