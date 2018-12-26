import aiohttp
import aioredis

async def fetch_token(config, rdsclient, session, logger):
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': config.get('appID'),
        'secret': config.get('appsecret'),
    }
    key = 'token'
    access_token = await rdsclient.get(key)
    if access_token is None:
        # Refresh token
        async with session.get(url, params=params) as resp:
            res = await resp.json()
        access_token = res.get('access_token')
        tr = rdsclient.multi_exec()
        tr.set(key, access_token)
        tr.pexpire(key, res.get('expires_in'))
        try:
            await tr.execute()
        except aioredis.MultiExecError:
            logger.error('FATAL ERROR in setting access token to redis')
    return access_token

