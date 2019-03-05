import re
from collections import defaultdict
import pathlib
import json

class Pipe:
    def __init__(self, function):
        self.f = function

    def __ror__(self, other):
        return self.f(other)

    def __call__(self, *args, **kwargs):
        return type(self)(lambda x: self.f(x, *args, **kwargs))

    def __get__(self, obj, typ=None):
        return type(self)(self.f.__get__(obj, typ))

class Mdreparser:
    def __init__(self):
        self.content = defaultdict(dict)
        self.r_hl1 = re.compile(r'^#+ (.+)')
        self.r_hls = re.compile(r'#{2,} (.+)')
        self.r_code = re.compile(r'(?s)`{3}(\w+)\n(.*?)\n`{3}\n')
        self.r_content = re.compile(r'\n(.*?)\n') # FIXME
        self.r_cmark = re.compile(r'[*`_\n]')

    @Pipe
    def parse_hl(self, content):
        self.content['title'] = self.r_hl1.findall(content)
        content = self.r_hl1.sub('', content)
        ihls = self.r_hls.finditer(content)
        hls = defaultdict(list)
        for hl in ihls:
            hl = hl.group(0).split(' ')
            level = len(hl[0])
            hl = hl[1].replace('`', '')
            hls[level].append(hl)
        content = self.r_hls.sub('', content)
        self.content.update({ "headline": hls })
        return content

    @Pipe
    def parse_code(self, content):
        icodes = self.r_code.findall(content)
        codes = defaultdict(list)
        for (lan, code) in icodes:
            codes[lan].append(code)
        content = self.r_code.sub('', content) 
        self.content.update({ "code": codes })
        return content
    
    @Pipe
    def parse_content(self, content):
        content = self.r_cmark.sub('', content)
        self.content.update({ "content": content })
        return content

    def parse(self, filename):
        with open(filename, 'r') as f:
            (f.read()
            | self.parse_hl()
            | self.parse_code() 
            | self.parse_content())
        return self.content

    def parseall(self, pathlst: list):
        for path in pathlst:
            path = pathlib.Path(path)
            for f in path.glob('*.md'):
                yield self.parse(f)

if __name__ == '__main__':
    fname = 'basic10.md'
    mdp = Mdreparser()
    #with open('test.json', 'w') as f:
    #    json.dump(mdp.content, f, indent=2, ensure_ascii=False)
