from flask import Flask, request, jsonify

import lark_oapi as lark
import lark_oapi.adapter.flask as lFlask
from controller.space_task_controller import SpaceTaskController

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


# 如果您的应用并不需要实时与用户交互结果，可以将这些任务与 HTTP 处理逻辑分离，交给另一个专注于后台任务处理的服务（如 Celery）。
# 这样就可以使得 Web 服务器专注于它最擅长的事情——处理尽可能多的 HTTP 请求，而不必为那些可异步处理的耗时任务而等待。

# 正常情况下，使用asyncio调用run，只是运行了事件循环，但flask不支持，也就等价于同步。
# 因此，还是需要采用asyncio.new_event_loop的方式，将接下来的处理交给事件循环。然后直接返回response。
# 没有及时接受到response，除此之外和隧道的性能也相关。后续部署到（飞书）云服务上。


app = Flask(__name__)

spaceTaskController = SpaceTaskController(space_id="7291489975366270978")

params = [
    "",  # encrypt_key
    "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0",  # verification_token
    lark.LogLevel.DEBUG
]


@app.route('/')
def index():
    return "Hello, World! Feishu Robot By linshaoqin"


@app.route('/event', methods=['POST'])
def handle_event():
    data = request.get_json()
    if 'type' in data and data['type'] == 'url_verification':
        print("[url_verification]" + data['challenge'])
        return jsonify({
            'challenge': data['challenge']
        })
    req = lFlask.parse_req()
    event_handler = lark.EventDispatcherHandler.builder(*params) \
        .register_p2_im_message_receive_v1(spaceTaskController.im_message_receive) \
        .register_p2_application_bot_menu_v6(spaceTaskController.bot_menu) \
        .build()
    lark.logger.info("[handle_event] " + lark.JSON.marshal(req.body, indent=4))
    resp = event_handler.do(lFlask.parse_req())
    return lFlask.parse_resp(resp)


@app.route('/card', methods=['POST'])
def handle_card():
    data = request.get_json()
    if 'type' in data and data['type'] == 'url_verification':
        print("[url_verification]" + data['challenge'])
        return jsonify({
            'challenge': data['challenge']
        })
    req = lFlask.parse_req()
    card_handler = lark.CardActionHandler.builder(*params) \
        .register(spaceTaskController.card_action) \
        .build()
    lark.logger.info("[handle_card] " + lark.JSON.marshal(req.body, indent=4))
    resp = card_handler.do(lFlask.parse_req())
    return lFlask.parse_resp(resp)


@app.after_request
def after_request(response):
    # todo 去重
    lark.logger.info("[after_request] " + lark.JSON.marshal(response.data, indent=4))
    return response


if __name__ == '__main__':
    app.run(port=5000, threaded=True)  # (host='192.168.0.107', port=5000) # sudo ufw allow 5000
