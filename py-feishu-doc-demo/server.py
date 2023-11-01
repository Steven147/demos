import os
import random
from flask import Flask, request, jsonify
import hashlib

import lark_oapi as lark
from lark_oapi.adapter.flask import *
from lark_oapi.api.im.v1 import *

app = Flask(__name__)


def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    print(lark.JSON.marshal(data))


def do_customized_event(data: lark.CustomizedEvent) -> None:
    print(lark.JSON.marshal(data))

handler = lark.EventDispatcherHandler.builder(lark.ENCRYPT_KEY, lark.VERIFICATION_TOKEN, lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p1_customized_event("message", do_customized_event) \
    .build()




@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/event", methods=["POST"])
def event():
    resp = handler.do(parse_req())
    return parse_resp(resp)


@app.route('/', methods=['POST'])
def handle_verification():
    data = request.get_json()
    if data['type'] == 'url_verification':
        return jsonify({
            'challenge': data['challenge']
        })

# def check_decode():
# 	bytes_b1 = (timestamp + nonce + encrypt_key).encode('utf-8')
# 	bytes_b = bytes_b1 + body
# 	h = hashlib.sha256(bytes_b)
# 	signature = h.hexdigest()
	# check if request headers['X-Lark-Signature'] equals to signature

if __name__ == '__main__':
    # ip = socket.gethostbyname(socket.gethostname()) todo get by socket
    app.run(port=5000)  # (host='192.168.0.107', port=5000) # sudo ufw allow 5000