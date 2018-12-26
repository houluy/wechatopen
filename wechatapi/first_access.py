from sanic import Blueprint, response
import hashlib

bp = Blueprint('access')

def __init__(config):
    @bp.route('/wechatapi')
    async def test(request):
        echostr = request.args.get('echostr')
        signature = request.args.get('signature')
        value = ''
        siglist = [config.get('token'), request.args.get('timestamp'), request.args.get('nonce')]
        siglist.sort()
        m = hashlib.sha1()
        m.update(''.join(siglist).encode())
        out = m.hexdigest()
        if out == signature:
            return response.raw(echostr.encode())
        else:
            print(out, signature)

