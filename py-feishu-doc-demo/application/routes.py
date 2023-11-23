from application import app
from flask import Flask, request, jsonify, render_template

import lark_oapi as lark
import lark_oapi.adapter.flask as lFlask
from controller.space_task_controller import SpaceTaskController

spaceTaskController = SpaceTaskController(space_id="7291489975366270978")

params = [
    "",  # encrypt_key
    "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0",  # verification_token
    lark.LogLevel.DEBUG
]


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'linshaoqin'}
    return render_template('index.html', title='Feishu Robot', user=user)


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
    # 没有及时接受到response，和隧道的性能也相关。后续部署到（飞书）云服务上。
    lark.logger.info("[after_request] " + lark.JSON.marshal(response.data, indent=4))
    return response
