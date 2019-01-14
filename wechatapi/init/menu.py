from ..req import get, post, store_token
import aiohttp

async def setupmenu(session, logger, token):
    data = {
        'button': [
            {
                'type': 'click',
                'name': '文章分类',
                'key': 'Category',
            },
            {
                'type': 'click',
                'name': '有问题吗',
                'key': 'Contact',
            },
        ]
    }

    res = await post('menu', session, logger, token, data=data)
    return res

