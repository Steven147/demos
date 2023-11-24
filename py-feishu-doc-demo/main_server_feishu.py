from application import app


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

# env | grep -E 'http_proxy|https_proxy'
# git config --global http.proxy 'http://127.0.0.1:7890'
# git config --global https.proxy 'http://127.0.0.1:7890'

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

# 如果你想要把你的 conda 环境中的 pip 包导出，可以使用以下的命令来生成一个 requirements.txt 文件：
# pip freeze > requirements.txt

# freeze 命令可以列出所有已安装的包及其准确的版本。这个命令把这个列表保存到一个叫做 requirements.txt 的文件中。
# 接着，如果你想在另外一个环境（比如你的服务器）安装这些包，你可以使用下面的 pip 命令来安装 requirements.txt 文件中列出的所有包：
# pip install -r requirements.txt

# flask run (python main_server_feishu.py)

# tutorial: [Introduction - The-Flask-Mega-Tutorial-zh](https://luhuisicnu.gitbook.io/the-flask-mega-tutorial-zh/)

# 数据库代码结构更新后，同步更新db文件结构：flask-migrate
# $ flask db migrate -m "posts table"
# $ flask db upgrade

# if __name__ == '__main__':
#     app.run()

