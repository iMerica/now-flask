from http.server import HTTPServer
import json
import requests
from __NOW_HANDLER_FILENAME import app
import _thread

# take advice from https://github.com/pallets/flask/issues/2995
from wsgiref.simple_server import make_server
server = make_server('0.0.0.0', 3000, app)
server.set_app(app)

def now_handler(event, context):
    _thread.start_new_thread(server.handle_request, ())
    payload = json.loads(event['body'])
    path = payload['path']
    headers = payload['headers']
    method = payload['method']
    
    res = requests.request(method, 'http://0.0.0.0:3000' + path, headers=headers)

    return {
        'statusCode': res.status_code,
        'headers': dict(res.headers),
        'body': res.text
    }

