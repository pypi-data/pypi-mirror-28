#!/usr/bin/env python

import asyncio
import random
import threading

import websockets
import aiofiles
from multiprocessing import Process
from aiohttp import web
import os


def logcc(websocket, path):
    f = yield from aiofiles.open('/tmp/logcc.log')
    try:
        while True:
            line = yield from f.readline()
            if not line:
                yield from asyncio.sleep(random.uniform(0, 1))
            else:
                line = line.strip()
                yield from websocket.send(line)

    finally:
        yield from f.close()


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

INDEX = open(os.path.join(__location__, 'index.html')).read().encode('utf-8')
JS = open(os.path.join(__location__, 'clusterize.min.js')).read().encode('utf-8')
CSS = open(os.path.join(__location__, 'clusterize.css')).read().encode('utf-8')


async def handle_index(request):
    return web.Response(body=INDEX, content_type='text/html')


async def handle_js(request):
    return web.Response(body=JS, content_type='text/javascript')


async def handle_css(request):
    return web.Response(body=CSS, content_type='text/css')


def run_websocket_server():
    start_server = websockets.serve(logcc, '127.0.0.1', 8989)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def run_http_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_get('/js', handle_js)
    app.router.add_get('/css', handle_css)
    web.run_app(app, host='127.0.0.1', port=8986)


p = Process(target=run_websocket_server)
p.start()
run_http_server()
p.join()
