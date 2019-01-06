from wechatapi import app
import yaml
import asyncio
from pprint import pprint
import aioredis

config_file = 'config/config.yml'
with open(config_file) as f:
    config = yaml.load(f)
app.conf = config.get('app')
loop = asyncio.get_event_loop()

app.run(**config.get('server'), debug=True, loop=loop)
