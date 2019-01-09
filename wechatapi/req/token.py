import aiohttp
import aioredis

async def store_token(config, rdsclient, session, logger, get):
    key = 'token'
    access_token = await rdsclient.get(key)
    if access_token is None:
        # Refresh token
        params = {
            'appid': config.get('appID'),
            'secret': config.get('appsecret'),
        }
        res = await get('token', session, logger, token='', extra_params=params)
        access_token = res.get('access_token')
        tr = rdsclient.multi_exec()
        tr.set(key, access_token)
        tr.pexpire(key, res.get('expires_in'))
        try:
            await tr.execute()
        except aioredis.MultiExecError:
            logger.error('FATAL ERROR in setting access token to redis')
    return access_token

