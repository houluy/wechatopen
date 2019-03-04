import yaml
import pathlib
import asyncio
from pprint import pprint
import json

import elasticsearch
import aiohttp

from wechatapi import app
from wechatapi.article import Article
from wechatapi.req import get, post, store_token

loop = asyncio.get_event_loop()
async def get_news():
    session = aiohttp.ClientSession(loop=loop)
    token_params = {
        'appid': 'wxb310e7246db43407',
        'secret': '7d183cd8402826fe432287d60bd03b2f',
    }
    token = (await get('token', session, '', token_params)).get('access_token')
    data = {
        'type': 'news',
        'offset': 0,
        'count': 1,
    }
    res = await post('material', session, token, data)
    await session.close()
    res = json.loads(res)
    res_list = res['item']
    for elem in res_list:
        for news in elem['content']['news_item']:
            news.pop('content')
    pprint(res)

loop.run_until_complete(get_news())
# Elasticsearch Initialization
elastic = elasticsearch.Elasticsearch()
indice = elasticsearch.client.IndicesClient(elastic)
# Create index

index_name = 'wechatopen'
index_settings = {
    "settings": {
        "analysis": {
            "analyzer": "jieba",
        }
    }
}

#print(indice.create(index=index_name, body=index_settings))

#art = Article(elastic, index_name)
#parent = pathlib.Path('It-is-not-only-Python')
#with open(parent / 'config', 'r') as f:
#    pathlst = [x.strip(' ').split(':') for x in f.read().split('\n')]
#    pathlst.pop()
#    pathlst = list(zip(*pathlst))
#    pathlst[0] = [parent / x for x in pathlst[0]]
#    art.initialize(pathlst[0])

#config_file = 'config/config.yml'
#with open(config_file) as f:
#    config = yaml.load(f)
#app.conf = config.get('app')
#
#app.run(**config.get('server'), debug=True)

