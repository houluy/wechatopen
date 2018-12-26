from sanic import Sanic, response
from sanic.log import logger
from wechatapi import fetch_token
import yaml
import aiohttp
import asyncio
import aioredis

config_file = 'config/config.yml'
with open(config_file) as f:
    config = yaml.load(f)

loop = asyncio.get_event_loop()
async def main():
    rdsclient = await aioredis.create_redis(
        'redis://localhost', loop=loop,
        encoding='utf8'
    )
    async with aiohttp.ClientSession() as session:
        print(await fetch_token(config, rdsclient, session, logger))

    rdsclient.close()
    await rdsclient.wait_closed()

loop.run_until_complete(main())

#async def f(config):
#    access = init(config)
#    print(await access())

#app = Sanic(__name__)
#app.blueprint(bp)
#
#app.run(host='0.0.0.0', port=80, debug=True)
