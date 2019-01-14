import aiohttp
import urllib.parse as up
from .token import store_token
import json

__all__ = ['get', 'post', 'store_token']

_baseurl = 'https://api.weixin.qq.com'
_openapi = {
    'token': {
        'endpoint': 'cgi-bin/token',
        'extra': {
            'grant_type': 'client_credential',
            'appid': '',
            'secret': '',
        },
    },
    'IP': {
        'endpoint': 'cgi-bin/getcallbackip',
    },
    'uinfo': {
        'endpoint': 'cgi-bin/user/info',
        'extra': {
            'openid': '',
            'lang': 'zh_CN',
        }
    },
    'ulist': {
        'endpoint': 'cgi-bin/user/get',
    },
    'usummary': {
        'endpoint': 'datacube/getusersummary',
        'data': {
            'begin_date': '',
            'end_date': '',
        },
    },
    'ucumulate': {
        'endpoint': 'datacube/getusercumulate',
        'data': {
            'begin_date': '',
            'end_date': '',
        },
    },
    'menu': {
        'endpoint': 'cgi-bin/menu/create',
    },
    'material': {
        'endpoint': 'cgi-bin/material/batchget_material',
        'data': {
            "type": '',
            "offset": '',
            "count": '',
        }
    },
}

def _fix_data(apiname, token, extra_params=None, data=None):
    api = _openapi[apiname]
    url = up.urljoin(_baseurl, api['endpoint'])
    try:
        extra = api['extra'].copy()
    except KeyError:
        extra = {}
    if extra_params is not None:
        extra.update(extra_params)
    try:
        extra_data = api['data'].copy()
    except KeyError:
        extra_data = {}
    if data is not None:
        extra_data.update(data)
    params = {
        'access_token': token,
        **extra,
    }
    return url, params, data

async def get(apiname, session, logger, token, extra_params=None):
    url, params, _ = _fix_data(apiname, token, extra_params)
    async with session.get(url, params=params) as resp:
        res = await resp.json()
    return res

async def post(apiname, session, logger, token, data, extra_params=None):
    url, params, data = _fix_data(apiname, token, extra_params, data)
    async with session.post(url, params=params, data=json.dumps(data, ensure_ascii=False).encode('utf8')) as resp:
        try:
            res = await resp.json()
        except aiohttp.client_exceptions.ContentTypeError:
            res = await resp.text()
    return res
