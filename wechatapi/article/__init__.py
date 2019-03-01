from .markdown import Mdreparser

class Article:
    def __init__(self, elastic, index_name):
        self.elastic = elastic
        self.markdown = Mdreparser()
        self.index = index_name
        self.doc = 'raw'
    
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
