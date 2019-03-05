async def get_news(count, offset, post):
    data = {
        'type': 'news',
        'offset': offset,
        'count': count,
    }
    res = await post('batchmaterial', data)
    res = json.loads(res)
    for elem in res['item']:
        for news in elem['content']['news_item']:
            news.pop('content')
    return res

async def get_materialcount(get):
    return await get('materialcount').get('news_count')

