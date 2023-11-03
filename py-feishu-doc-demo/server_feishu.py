import os
import random
from flask import Flask, request, jsonify
import hashlib
import json

from typing import Optional
import lark_oapi as lark
import lark_oapi.adapter.flask as lFlask
import lark_oapi.api.im.v1 as imV1
from feishu_main import output_wrapper

from threading import Thread
import asyncio

# 请确保您的工作目录正确
# cd /home/natfrp/

# 生成 KDF 后的远程管理 E2E 密码，复制输出的 Base64 字符串备用
# ./natfrp-service remote-kdf <您的远程管理 E2E 密码> frp+6

# 编辑配置文件, 以 vim 为例
# vim .config/natfrp-service/config.json

# systemctl enable --now natfrp.service
# systemctl status natfrp.service

# # 查看日志，确认看到 "远程管理连接成功" 的输出
# journalctl -u natfrp.service -f
# [远程管理 | SakuraFrp](https://www.natfrp.com/remote/v2)

# cd /DATA/Documents/demos/py-feishu-doc-demo
# conda config --set auto_activate_base [true]
# source ~/.bashrc
# conda create -y -n feishu-robot python=3.9
# conda activate feishu-robot
# pip install lark_oapi reportlab pdfrw pdf2image flask

# python server_feishu.py 

# tmux attach -t feishu-robot-session


app = Flask(__name__)


def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

new_loop = asyncio.new_event_loop()
t = Thread(target= start_thread_loop, args=(new_loop,))
t.start()



def do_p2_im_message_receive_v1(data: imV1.P2ImMessageReceiveV1) -> None:
    if not data or \
        not data.event or \
        not data.event.message or \
        not data.event.message.content: return
    ctt = json.loads(data.event.message.content)
    if 'text' in ctt and ctt['text'] == '/output_all_file':
        if not data.event.sender or \
            not data.event.sender.sender_id or \
            not data.event.sender.sender_id.user_id: return
        new_loop.call_soon_threadsafe(output_wrapper, data.event.sender.sender_id.user_id)
    print("do_p2_im_message_receive_v1: \n")

def do_customized_event(data: lark.CustomizedEvent) -> None:
    print(lark.JSON.marshal(data))

handler = lark.EventDispatcherHandler.builder("", "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0", lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p1_customized_event("message", do_customized_event) \
    .build()




@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/event', methods=['POST'])
def handle_verification():
    data = request.get_json()
    if 'type' in data and data['type'] == 'url_verification':
        print(data)
        return jsonify({
            'challenge': data['challenge']
        })
    
    resp = handler.do(lFlask.parse_req())
    return lFlask.parse_resp(resp)

# def check_decode():
# 	bytes_b1 = (timestamp + nonce + encrypt_key).encode('utf-8')
# 	bytes_b = bytes_b1 + body
# 	h = hashlib.sha256(bytes_b)
# 	signature = h.hexdigest()
	# check if request headers['X-Lark-Signature'] equals to signature

if __name__ == '__main__':
    # ip = socket.gethostbyname(socket.gethostname()) todo get by socket
    app.run(port=5000)  # (host='192.168.0.107', port=5000) # sudo ufw allow 5000