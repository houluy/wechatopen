import unittest
import xmltodict
import json

class TestMessage(unittest.TestCase):
    def test_text(self):
        text = '<xml><URL><![CDATA[http://lucima.cn/wechatapi]]></URL><ToUserName><![CDATA[gh_4880aedc8c37]]></ToUserName><FromUserName><![CDATA[1]]></FromUserName><CreateTime>123</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[hello]]></Content><MsgId>123</MsgId></xml>'
        dic = xmltodict.parse(text)
        self.assertEqual(dic, {
            "xml": {
                "URL": "http://lucima.cn/wechatapi",
                "ToUserName": "gh_4880aedc8c37",
                "FromUserName": "1",
                "CreateTime": "123",
                "MsgType": "text",
                "Content": "hello",
                "MsgId": "123"
            }
        })

