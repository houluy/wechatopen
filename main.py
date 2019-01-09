from wechatapi import app
import yaml
from pprint import pprint
import aioredis

config_file = 'config/config.yml'
with open(config_file) as f:
    config = yaml.load(f)
app.conf = config.get('app')

app.run(**config.get('server'), debug=True)
