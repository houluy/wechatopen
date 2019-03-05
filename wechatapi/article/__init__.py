from .markdown import Mdreparser
from .articleid import get_news, get_materialcount

class Article:
    BATCH_COUNT = 20
    def __init__(self, elastic, index_name, get, post):
        self.elastic = elastic
        self.markdown = Mdreparser()
        self.index = index_name
        self.doc = 'raw'
        self.get = get
        self.post = post
    
    def initialize(self, pathlst):
        for ind, items in enumerate(self.markdown.parseall(pathlst)):
            try:
                self.elastic.create(
                    index=self.index,
                    doc_type=self.doc,
                    id=ind,
                    body=items
                )
            except Exception as e:
                print(e)
            else:
                print(f'Body {ind} created successfully')
        total_num = get_materialcount(self.get)
        rnd = total_num % self.BATCH_COUNT
        for ind in range(rnd):
            offset = ind * self.BATCH_COUNT
            count = self.BATCH_COUNT
            res = get_news(count, offset, self.post)

        
