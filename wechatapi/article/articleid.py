from wechatapi.req import post

async def get_news(count, offset, loop, session, token):
    data = {
        'type': 'news',
        'offset': offset,
        'count': count,
    }
    res = await post('material', session, token, data)
    res = json.loads(res)
    ret = {}
    for key, value in res.items():
        if key == 'item':
            ret[key] = []
            for item in value:
                for k, v in item.items():
                    if k == 'content':
                        continue

        else:
            print(key, value)



