import unittest
import re
from wechatapi.article.markdown import Mdreparser

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.test_string = """# 测试`code`

## 二级标题

这是**正文**，这是行内代码`inline`。

```python
# Python code
print('hello world')
```

### 三级标题`code`

这是第二段**正文**，这是行内代码`inline`。

```python
import re
re.compile('hi')
```

### 另一个三级标题

```C
#include <stdio.h>
```

"""
        self.markdown = Mdreparser()

    def test_parse_title(self):
        self.markdown.parse_hl().f(self.test_string)
        self.assertEqual(self.markdown.content.get('title'), '测试code')

    def test_parse_hls(self):
        self.markdown.parse_hl().f(self.test_string)
        image_headline = {
            2: ['二级标题'],
            3: ['三级标题code', '另一个三级标题'],
        }
        self.assertEqual(self.markdown.content.get('headline'), image_headline)

    def test_parse_code(self):
        self.markdown.parse_code().f(self.test_string)
        image_code = {
            'python': ["# Python code\nprint('hello world')", "import re\nre.compile('hi')"],
            'C': ["#include <stdio.h>"],
        }
        self.assertEqual(self.markdown.content.get('code'), image_code)

    def test_parse_content(self):
        (self.test_string
        | self.markdown.parse_hl()
        | self.markdown.parse_code()
        | self.markdown.parse_content())
        image_content = '这是正文，这是行内代码inline。这是第二段正文，这是行内代码inline。'
        self.assertEqual(self.markdown.content.get('content'), image_content)
