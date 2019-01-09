import xmltodict
import time
from pprint import pprint

__all__ = ['registry']

registry = {}
eventregistry = {}

def dispatch(typ):
    def clsfac(cls):
        handler = cls()
        if typ != 'event':
            registry[typ] = handler._respond
        else:
            registry[typ] = handler.assign
        return cls
    return clsfac

@dispatch('')
class BaseHandler:
    def _respond(self, params, message, text):
        resdic = {
            'xml': {
                'ToUserName': params.get('openid'),
                'FromUserName': message.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': text,
            }
        }
        resmsg = xmltodict.unparse(resdic)
        return resmsg.encode()

@dispatch('event')
class EventHandler(BaseHandler):
    @classmethod
    def subdispatch(cls, event):
        def subclsfac(subcls):
            handler = subcls()
            eventregistry[event] = handler._respond
            return subcls
        return subclsfac

    @staticmethod
    def assign(params, message):
        return eventregistry[message.get('Event')](params, message)

@EventHandler.subdispatch('subscribe')
class Subscription(EventHandler):
    def _respond(self, params, message):
        text = 'welcome'
        return super()._respond(params, message, text)

@EventHandler.subdispatch('unsubscribe')
class Unsubscription(EventHandler):
    def _respond(self, params, message):
        text = 'GoodBye'
        return super()._respond(params, message, text)

@dispatch('location')
class UploadGeo(EventHandler):
    def _respond(self, params, message):
        text = ''
        self.handle(params, message)
        return super()._respond(params, message, text)

    def handle(self, params, message):
        pprint(message)

@dispatch('text')
class TextHandler(BaseHandler):
    def _respond(self, params, message):
        text = 'hello'
        return super()._respond(params, message, text)

