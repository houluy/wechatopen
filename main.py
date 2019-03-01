import yaml
import pathlib

import elasticsearch

from wechatapi import app
from wechatapi.article import Article
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

