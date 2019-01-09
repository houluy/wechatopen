import aioredis
import asyncio
import unittest

class TestAioRedis(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.key = 'token_test'

    def test_op(self):
        async def go():
            redis = await aioredis.create_redis(
                'redis://localhost', loop=self.loop,
                encoding='utf8'
            )
            dic = {
                'value': '123',
                'exp': '100',
            }
            await redis.hmset_dict(self.key, dic)

            val = await redis.hgetall(self.key)

            self.assertEqual(val, dic)
            redis.close()
            await redis.wait_closed()
        self.loop.run_until_complete(go())

    def test_expire(self):
        async def go():
            redis = await aioredis.create_redis(
                'redis://localhost', loop=self.loop,
                encoding='utf8'
            )
            value = '123'
            tr = redis.multi_exec()
            tr.set('value', value)
            tr.pexpire('value', 2000)
            try:
                await tr.execute() 
            except aioredis.MultiExecError:
                pass
            
            val = await redis.get('value')
            self.assertEqual(val, value)
            await asyncio.sleep(2)
            val = await redis.get('value')
            self.assertEqual(val, None)
        self.loop.run_until_complete(go())

    def tearDown(self):
        async def go():
            redis = await aioredis.create_redis(
                'redis://localhost', loop=self.loop,
                encoding='utf8'
            )
            await redis.delete(self.key)
        self.loop.run_until_complete(go())
