# -*- coding: utf-8 -*-
from doc_funcs import *
from create_watermark import trans_to_watermark_file
import time

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
        download_export_task_request_wrapper(client, file_token, output_dir='input_file')

def output_wrapper(user_id: str):
    app_id = 'cli_a5bb0a8ac8f99013'
    app_secret = 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'
    root_dir = os.path.dirname(__file__)
    input_dir = os.path.join(root_dir, 'input_file')
    output_dir = os.path.join(root_dir, 'output_file')  # 新建文件路径指向 output 文件夹

    need_update = False
    need_upload = False
    space_id = '7291489975366270978'
    parent_node = 'LU46wq2kIixvGVkfenqcX4bMnfc' #【文档】“我们是中国的未来”孝亲反哺专场第8期
    obj_token = "FgBmdX4YioQsacxNkpUcMiUmnmh"
            # "space_id": "7291489975366270978",
            # "node_token": "LU46wq2kIixvGVkfenqcX4bMnfc",
            # "obj_token": "FgBmdX4YioQsacxNkpUcMiUmnmh",

    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.ERROR) \
        .build()
    
    # list_space_request_wrapper(client)
    # get_space_request_wrapper(client, '7291489975366270978')
    # list_space_node_request_wrapper(client, '7291489975366270978')  root node
    # list_space_node_request_wrapper(client, '7291489975366270978', 'OEecwNC8nipwKekmM1wcJRgZno9') # 首页 node
    # list_space_node_request_wrapper(client, '7291489975366270978', 'P3m9wICTii7egIkB9vLcEnkPnic') # 遍历 芳芳老师文档整理
    # create_document_request_wrapper(client, "", "new doc")
    # move_docs_to_wiki_space_node_request_wrapper(client, 7291489975366270978, 'LU46wq2kIixvGVkfenqcX4bMnfc', obj_token= 'EW9LdimcWodD6NxOUgHcOTi2nOb')

    create_message_request_wrapper(client, receive_id_type="user_id",receive_id=user_id, msg_type="text", content="{\"text\":\"processing...\"}")
    if need_update:
        nodes = list_space_node_request_wrapper(client, space_id, parent_node) # 遍历 
        if nodes: 
            for node in nodes:
                export_file(client, node.obj_token)
            
        trans_to_watermark_file(
            name='爱与幸福文字中心', 
            input_dir=input_dir, 
            output_dir=output_dir,
            )
        
    if need_upload:
        create_message_request_wrapper(client, receive_id_type="user_id",receive_id=user_id, msg_type="text", content="{\"text\":\"all files output\"}")
        for dir_path, dirnames, file_names in os.walk(output_dir):
            for file_name in sorted(file_names):
                file_path = os.path.join(dir_path, file_name)
                # file_token = upload_all_media_request_wrapper(
                #         client=client,
                #         file_name=file_name,
                #         file_path=file_path,
                #         parent_type='docx_file',
                #         parent_node=obj_token
                #     )
                # block_id = create_document_block_children_request_wrapper(client, document_id=obj_token, block_id=obj_token)
                # patch_document_block_request_wrapper(client, document_id=obj_token, block_id=block_id, file_token=file_token)
                # file_tokens.append(file_token)

                file_key = create_file_request_wrapper(client, file_name, file_path)
                content = "{\"file_key\":\"%s\"}" % file_key
                create_message_request_wrapper(client, receive_id_type="user_id",receive_id=user_id, msg_type="file", content=content)
                # create_message_request_wrapper(client, receive_id_type="user_id",receive_id="ca4ba8a3", msg_type="file", content=content)
                # ca4ba8a3
                

    # for file_token in file_tokens:
        
        # patch_document_block_request_wrapper(client, document_id=obj_token, block_id=block_id, file_token=file_token)
        
def send_card(user_id: str):
    app_id = 'cli_a5bb0a8ac8f99013'
    app_secret = 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.ERROR) \
        .build()
    create_message_request_wrapper(
        client,
        receive_id_type="user_id",
        receive_id=user_id,
        msg_type="interactive",
        content="{\"config\":{\"wide_screen_mode\":true},\"header\":{\"template\":\"blue\",\"title\":{"
                "\"tag\":\"plain_text\",\"content\":\"文档编码生成卡片\"}},\"card_link\":{\"url\":\"\",\"pc_url\":\"\","
                "\"android_url\":\"\",\"ios_url\":\"\"},\"elements\":[{\"tag\":\"div\",\"text\":{\"tag\":\"lark_md\","
                "\"content\":\"请输入文档分类\"},\"extra\":{\"tag\":\"select_static\",\"placeholder\":{"
                "\"tag\":\"plain_text\",\"content\":\"文档分类\"},\"value\":{\"key\":\"category\"},\"options\":[{"
                "\"text\":{\"tag\":\"plain_text\",\"content\":\"秘笈A\"},\"value\":\"秘笈A\"},{\"text\":{"
                "\"tag\":\"plain_text\",\"content\":\"表达B\"},\"value\":\"表达B\"},{\"text\":{\"tag\":\"plain_text\","
                "\"content\":\"行为C\"},\"value\":\"行为C\"},{\"text\":{\"tag\":\"plain_text\",\"content\":\"操作D\"},"
                "\"value\":\"操作D\"}]}},{\"tag\":\"div\",\"text\":{\"tag\":\"lark_md\",\"content\":\"请输入版块\"},"
                "\"extra\":{\"tag\":\"select_static\",\"placeholder\":{\"tag\":\"plain_text\",\"content\":\"版块\"},"
                "\"value\":{\"key\":\"section\"},\"options\":[{\"text\":{\"tag\":\"plain_text\","
                "\"content\":\"爱相伴01\"},\"value\":\"爱相伴01\"},{\"text\":{\"tag\":\"plain_text\","
                "\"content\":\"爱相随02\"},\"value\":\"爱相随02\"},{\"text\":{\"tag\":\"plain_text\","
                "\"content\":\"爱相遇03\"},\"value\":\"爱相遇03\"},{\"text\":{\"tag\":\"plain_text\","
                "\"content\":\"爱未来04\"},\"value\":\"爱未来04\"}]}},{\"tag\":\"div\",\"text\":{\"tag\":\"lark_md\","
                "\"content\":\"请输入关系\"},\"extra\":{\"tag\":\"select_static\",\"placeholder\":{\"tag\":\"plain_text\","
                "\"content\":\"关系\"},\"value\":{\"key\":\"relationship\"},\"options\":[{\"text\":{"
                "\"tag\":\"plain_text\",\"content\":\"生命成长类\"},\"value\":\"生命成长类\"},{\"text\":{"
                "\"tag\":\"plain_text\",\"content\":\"亲子关系类\"},\"value\":\"亲子关系类\"},{\"text\":{"
                "\"tag\":\"plain_text\",\"content\":\"孝亲关系类\"},\"value\":\"孝亲关系类\"},{\"text\":{"
                "\"tag\":\"plain_text\",\"content\":\"夫妻关系类\"},\"value\":\"夫妻关系类\"}]}},{\"tag\":\"div\","
                "\"text\":{\"tag\":\"lark_md\","
                "\"content\":\"选择完成后，点击确认，会自动生成文档对应的**编码**。\\n同时会以编码作为标题在知识库中新建文档，返回文档**链接**。\"},\"extra\":{"
                "\"tag\":\"button\",\"text\":{\"tag\":\"lark_md\",\"content\":\"确认\"},\"type\":\"primary\","
                "\"value\":{\"key\":\"confirm\"}}}]}"
    )
    # patch_message_request_wrapper(client)

# 调用
def main():
    output_wrapper("92e9d9e9") # send to me
    
if __name__ == "__main__":
    main()