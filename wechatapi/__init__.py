#from .first_access import __init__, bp
from .token import fetch_token
from .ips import fetch_IP
from .event.handler import *
from sanic import Sanic, response
from sanic.log import logger
from .event.handler import registry
import xmltodict
import time
import json
import aiohttp
import asyncio
import aioredis
import hashlib

app = Sanic(__name__)

@app.listener('before_server_start')
async def setup(app, loop):
    redis = await aioredis.create_redis(
        'redis://localhost', loop=loop,
        encoding='utf8'
    )
    app.redis = redis
    app.session = aiohttp.ClientSession(loop=loop)

@app.listener('after_server_start')
async def notify_startup(app, loop):
    with open('config/banner', 'r') as f:
        banner = f.read()
    print(banner)

@app.listener('after_server_stop')
async def teardown(app, loop):
    app.redis.close()
    await app.redis.wait_closed()
    await app.session.close()

# Message verification
@app.middleware('request')
async def verification(request):
    params = request.args

# Token middleware
@app.middleware('request')
async def token(request):
    access_token = await fetch_token(request.app.conf, request.app.redis, request.app.session, logger)
    request.app.access_token = access_token

@app.route('/wechatapi', methods=['GET',])
async def test(request):
    echostr = request.args.get('echostr')
    signature = request.args.get('signature')
    value = ''
    siglist = [request.app.conf.get('token'), request.args.get('timestamp'), request.args.get('nonce')]
    siglist.sort()
    m = hashlib.sha1()
    m.update(''.join(siglist).encode())
    out = m.hexdigest()
    if out == signature:
        return response.raw(echostr.encode())
    else:
        print(out, signature)

@app.route('/wechatapi', methods=['POST',])
async def message(request):
    params = request.args
    message = xmltodict.parse(request.body.decode())
    message = message.get('xml')
    msgtype = message.get('MsgType')
    print(message)
    return response.raw(registry.get(msgtype)(params, message))

