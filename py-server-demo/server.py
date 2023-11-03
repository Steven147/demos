import os
import random
from flask import Flask, send_file

app = Flask(__name__)

# $ source /DATA/Documents/demos/py-server-demo/bin/activate
# $ cd ~/Documents/demos/py-server-demo
# ls
# python server.py

# 获取 image 目录下的所有视频文件列表
image_dir = '/DATA/Gallery/'  # image 文件夹的路径
prefix_url = '/image/'

# video_files = os.listdir(image_dir)

@app.route('/')
def index():
    return 'Hello, World!'

# @app.route('/video')
# def video():
#     filename = random.choice(video_files)  # 随机获取一个视频文件名
#     filepath = os.path.join(video_dir, filename)  # 获取视频文件的完整路径
#     print("[Info] request video, filename" + filename)
#     return send_file(filepath, mimetype='image/jpg')  # 返回视频文件

@app.route('/images/<count>')
def images(count):
    count = int(count)
    files = os.listdir(image_dir)
    image_urls = [f"{prefix_url}{file}" for file in files if file.endswith('.jpg')]
    if len(image_urls) < count:
        jsonify({'error': 'File not enough'})
    else:
        image_urls = random.sample(image_urls, count)
        return {'image_urls': image_urls}

@app.route(prefix_url + '<name>')
def get_image(name):
    prefix_url = '/static/images/'
    filepath = os.path.join(image_dir, name)
    if os.path.exists(filepath):
        url = prefix_url + name
        return send_file(filepath, mimetype='image/jpg')
    else:
        return jsonify({'error': 'File not found'})


if __name__ == '__main__':
    # ip = socket.gethostbyname(socket.gethostname()) todo get by socket
    app.run(host='192.168.0.107', port=5000) # sudo ufw allow 5000