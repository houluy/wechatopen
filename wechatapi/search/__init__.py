import elasticsearch
from pprint import pprint

class Search:
    def __init__(self, elastic):
        self.elastic = elastic

    def search_body(self, keywords):
        body = {
            'query': {
                'bool': {
                    'must': {
                        'query_string': {
                            'query': keywords,
                        }
                    }
                }
            }
        }
        body = {
            'from': 0,
            'size': 5,
            '_source': False,
            'query': {
                'match': {
                    'content': keywords,
                }
            }
        }
        pprint(self.elastic.search(
            index='wechatopen',
            doc_type='raw',
            body=body
        ))

if __name__ == '__main__':
    elastic = elasticsearch.Elasticsearch()
    indices = elasticsearch.client.IndicesClient(elastic)
    s = Search(elastic)
    #settings = {
    #    "settings": {
    #        "analysis": {
    #            "analyzer": "jieba",
    #        }
    #    }
    #}
    #print(indices.put_settings(body=settings, index="wechatopen"))
    s.search_body('函数')
