import requests



def post(offset, count, NO_CONTENT):
    url = "https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token=%s"%(ACCESS_TOKEN)
    value = {}
    value["offset"] = offset
    value["count"] = count
    value["no_content"] = NO_CONTENT
    response = requests.post(url, value)
    print(response.text)
    
    
if __name__ == "__main__":
	ACCESS_TOKEN = None # TODO 获取tk
	NO_CONTENT = 0 # 正常返回
	AppID = "wx18d791a0097543cf"
	count_all = 2899
	max_once = 20

	for i in range(0, count_all, max_once): # 0-2898
		post(i, max_once, NO_CONTENT)
    