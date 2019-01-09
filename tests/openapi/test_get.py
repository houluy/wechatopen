import asyncio
import aioredis
import aiohttp
import unittest
import time
from wechatapi import req

class TestOpenApi(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        async def asyncsetup():
            self.redis = await aioredis.create_redis(
                'redis://localhost',
                loop=self.loop,
                encoding='utf8',
            )
            self.session = aiohttp.ClientSession(loop=self.loop)
            self.token_params = {
                'appid': 'wxfd9d573162c4d085',
                'secret': '7a73b7351a3ffaa91dc62f36f715b60d',
            }
            self.token = (await req.get('token', self.session, None, '', self.token_params)).get('access_token')
        self.loop.run_until_complete(asyncsetup())

    def test_IP(self):
        async def IP():
            res = await req.get('IP', self.session, None, self.token)
            self.assertTrue('ip_list' in res)
        self.loop.run_until_complete(IP()) 

    def test_ulist(self):
        async def ulist():
            res = await req.get('ulist', self.session, None, self.token)
            self.assertTrue('total' in res)
        self.loop.run_until_complete(ulist()) 

    def test_uinfo(self):
        openid = 'otpUm5zU8a6L2YkCR4Qx0rSgH4qk'
        async def uinfo():
            params = {
                'openid': openid,
            }
            res = await req.get('uinfo', self.session, None, self.token, params)
            self.assertTrue('openid' in res)
        self.loop.run_until_complete(uinfo()) 

    def test_usummary(self):
        async def usummary():
            data = {
                'begin_date': '2018-12-11',
                'end_date': '2018-12-11',
            }
            res = await req.post('usummary', self.session, None, self.token, data=data)
            self.assertTrue('list' in res)
        self.loop.run_until_complete(usummary())

    def test_ucumulate(self):
        async def ucumulate():
            data = {
                'begin_date': '2018-12-11',
                'end_date': '2018-12-11',
            }
            res = await req.post('ucumulate', self.session, None, self.token, data=data)
            self.assertTrue('list' in res)
        self.loop.run_until_complete(ucumulate())

    def tearDown(self):
        async def asyncteardown():
            self.redis.close()
            await self.redis.wait_closed()
            await self.session.close()
        self.loop.run_until_complete(asyncteardown())

