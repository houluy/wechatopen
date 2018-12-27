import aiohttp

async def fetch_IP(session, logger, token):
    url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip'
    params = {
        'access_token': token,
    }

    async with session.get(url, params=params) as resp:
        res = await resp.json()

    return res
