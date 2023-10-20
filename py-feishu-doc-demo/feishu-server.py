import requests
import json

TOKEN_FILE = 'token.json'  # 保存token的文件名

def request_access_token(app_id, app_secret):
    headers = {'Content-Type': 'application/json'}

    data = {"app_id": app_id, "app_secret": app_secret}
    data_json = json.dumps(data)

    response = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers=headers, data=data_json)
    if response.status_code == 200:
        token_data = response.json()  # 解析响应数据
        token_data_str = json.dumps(token_data)  # 将字典对象转为json字符串
        with open(TOKEN_FILE, 'w') as f:
            f.write(token_data_str)  # 将获取到的token信息写入到文件中
        return token_data['tenant_access_token']  # 返回获取到的token
    else:
        print('Error:', response.status_code, response.text)

def get_access_token():
    access_token = ''
    try:
        with open(TOKEN_FILE, 'r') as f:
            token_data_str = f.read()  # 从文件中读取token信息
            token_data = json.loads(token_data_str)  # 将json字符串转换为字典对象
            access_token = token_data['tenant_access_token']
    except FileNotFoundError:
        pass
    return access_token

# 调用示例
app_id = 'cli_a5bb0a8ac8f99013'
app_secret = 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'
token = get_access_token()
if not token:
    token = request_access_token(app_id, app_secret)
print('当前token为：', token)