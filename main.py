from sanic import Sanic, response
from sanic.log import logger
from wechatapi import fetch_token, fetch_IP
import yaml
import aiohttp
import asyncio
import aioredis
import xmltodict
import json
import time
from pprint import pprint

config_file = 'config/config.yml'
with open(config_file) as f:
    config = yaml.load(f)
app = Sanic(__name__)
loop = asyncio.get_event_loop()

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

@app.listener('before_server_stop')
async def teardown(app, loop):
    app.redis.close()
    await app.redis.wait_closed()
    app.session.close()


# Message verification
@app.middleware('request')
async def verification(request):
    params = request.args

# Token middleware
@app.middleware('request')
async def token(request):
    access_token = await fetch_token(config, request.app.redis, request.app.session, logger)
    request.app.access_token = access_token

@app.route('/wechatapi', methods=['POST',])
async def message(request):
    params = request.args
    message = xmltodict.parse(request.body.decode())
    message = message.get('xml')
    resdic = {
        'xml': {
            'ToUserName': params.get('openid'),
            'FromUserName': message.get('ToUserName'),
            'CreateTime': int(time.time()),
            'MsgType': 'text',
            'Content': 'hi',
        }
    }
    resmsg = xmltodict.unparse(resdic)
    return response.raw(resmsg.encode())

app.run(host='0.0.0.0', port=80, debug=True, loop=loop)

