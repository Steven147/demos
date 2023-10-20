from space_funcs import *
from doc_funcs import *
import time


# 调用
def main():

    app_id = 'cli_a5bb0a8ac8f99013'
    app_secret = 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'

    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()
    
    # list_space_request_wrapper(client)
    # get_space_request_wrapper(client, '7291489975366270978')
    # list_space_node_request_wrapper(client, '7291489975366270978')  root node
    # list_space_node_request_wrapper(client, '7291489975366270978', 'OEecwNC8nipwKekmM1wcJRgZno9') 首页 node
    # list_space_node_request_wrapper(client, '7291489975366270978', 'P3m9wICTii7egIkB9vLcEnkPnic') # 遍历 芳芳老师文档整理
    # list_space_node_request_wrapper(client, '7291489975366270978', 'LU46wq2kIixvGVkfenqcX4bMnfc') # 遍历 【文档】“我们是中国的未来”孝亲反哺专场第8期
    # create_document_request_wrapper(client, "", "new doc")
    # move_docs_to_wiki_space_node_request_wrapper(client, 7291489975366270978, 'LU46wq2kIixvGVkfenqcX4bMnfc', obj_token= 'EW9LdimcWodD6NxOUgHcOTi2nOb')

    token = 'Xy9XdNqo2oZYj7xP7DEcg9rundd'
    export_file(client, token)

def export_file(client, token):
    attempts = 0   # 初始化轮询计数器
    max_attempts=5
    interval=1

    ticket = create_export_task_request_wrapper(client, ext="pdf", token=token, type='docx')
    if ticket == None: 
        return
    
    file_token = None # 初始化最后一次轮询的结果 
    while attempts < max_attempts:
        file_token = get_export_task_request_wrapper(client, ticket, token) 
        if file_token: break
        attempts += 1   # 增加轮询计数器
        time.sleep(interval*attempts)   # 添加轮询间隔等待时间
    
    if file_token:
        download_export_task_request_wrapper(client, file_token)


if __name__ == "__main__":
    main()