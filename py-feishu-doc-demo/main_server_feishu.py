from flask import Flask, request, jsonify
import json

import lark_oapi as lark
import lark_oapi.adapter.flask as lFlask
import lark_oapi.api.im.v1 as imV1
from lark_oapi.api.application.v6.model.p2_application_bot_menu_v6 import P2ApplicationBotMenuV6
from main_feishu import output_wrapper, get_code_params, update_card, send_code_params_guide, new_code_params, \
    new_code_title_prefix, search_code_prefix, multi_search_code_prefix, output_code_prefix, multi_output_code_prefix, \
    output_func, multi_get_code_params, multi_output_func

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

# python main_server_feishu.py

# tmux attach -t feishu-robot-session
# cd /DATA/Documents/demos/py-feishu-doc-demo
# conda activate feishu-robot
# python main_server_feishu.py


app = Flask(__name__)


def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


new_loop = asyncio.new_event_loop()
t = Thread(target=start_thread_loop, args=(new_loop,))
t.start()


def do_p2_im_message_receive_v1(data: imV1.P2ImMessageReceiveV1) -> None:
    if not data.event.message.content or \
            not data.event.sender.sender_id.user_id:
        return
    ctt = json.loads(data.event.message.content)
    user_id = data.event.sender.sender_id.user_id
    if user_id and 'text' in ctt:
        content = ctt['text']
        if content in ['help', '/help', '帮助']:
            # new_loop.call_soon_threadsafe(output_wrapper, data.event.sender.sender_id.user_id)
            new_loop.call_soon_threadsafe(send_code_params_guide, user_id)
        elif content.startswith(new_code_title_prefix):
            new_loop.call_soon_threadsafe(new_code_params, content, user_id)
        elif content.startswith(search_code_prefix):
            new_loop.call_soon_threadsafe(get_code_params, content, user_id)
        elif content.startswith(multi_search_code_prefix):
            new_loop.call_soon_threadsafe(multi_get_code_params, content, user_id)
        elif content.startswith(output_code_prefix):
            new_loop.call_soon_threadsafe(output_func, content, user_id)
        elif content.startswith(multi_output_code_prefix):
            new_loop.call_soon_threadsafe(multi_output_func, content, user_id)
        # new_loop.call_soon_threadsafe(get_code_params, ctt['text'], data.event.sender.sender_id.user_id)
    print("do_p2_im_message_receive_v1: \n" + str(data))


def do_p2_application_bot_menu_v6(data: P2ApplicationBotMenuV6) -> None:
    key = data.event.event_key
    if key == "menu0201":
        new_loop.call_soon_threadsafe(send_code_params_guide, data.event.operator.operator_id.user_id)
    if key == "menu0301":
        new_loop.call_soon_threadsafe(output_wrapper, data.event.operator.operator_id.user_id)
    print("do_p2_application_bot_menu_v6: \n")


def do_customized_event(data: lark.CustomizedEvent) -> None:
    print(lark.JSON.marshal(data))


token = "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0"

handler = lark.EventDispatcherHandler.builder("", token, lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p2_application_bot_menu_v6(do_p2_application_bot_menu_v6) \
    .register_p1_customized_event("message", do_customized_event) \
    .build()


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/event', methods=['POST'])
def handle_event():
    print("[handle_event] ---call---")
    data = request.get_json()
    if 'type' in data and data['type'] == 'url_verification':
        print("[url_verification]" + data['challenge'])
        return jsonify({
            'challenge': data['challenge']
        })

    if 'token' in data \
            and data['token'] != token \
            and 'action' in data:
        print("[update_card] call" + str(data))
        new_loop.call_soon_threadsafe(update_card, data)
        return jsonify({"message": "Data received successfully"}), 200

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
    app.run(port=5000, threaded=True)  # (host='192.168.0.107', port=5000) # sudo ufw allow 5000
