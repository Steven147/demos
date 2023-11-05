# -*- coding: utf-8 -*-
from doc_funcs import *
from create_watermark import trans_to_watermark_file
from database.coding_funcs import get_card_source_string, get_next_document_number, Document
import time


def export_file(client, token):
    attempts = 0  # 初始化轮询计数器
    max_attempts = 5
    interval = 1

    ticket = create_export_task_request_wrapper(client, ext="pdf", token=token, type='docx')
    if ticket == None:
        return

    file_token = None  # 初始化最后一次轮询的结果
    while attempts < max_attempts:
        file_token = get_export_task_request_wrapper(client, ticket, token)
        if file_token: break
        attempts += 1  # 增加轮询计数器
        time.sleep(interval * attempts)  # 添加轮询间隔等待时间

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
    parent_node = 'LU46wq2kIixvGVkfenqcX4bMnfc'  # 【文档】“我们是中国的未来”孝亲反哺专场第8期
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

    create_message_request_wrapper(client, receive_id_type="user_id", receive_id=user_id, msg_type="text",
                                   content="{\"text\":\"processing...\"}")
    if need_update:
        nodes = list_space_node_request_wrapper(client, space_id, parent_node)  # 遍历
        if nodes:
            for node in nodes:
                export_file(client, node.obj_token)

        trans_to_watermark_file(
            name='爱与幸福文字中心',
            input_dir=input_dir,
            output_dir=output_dir,
        )

    if need_upload:
        create_message_request_wrapper(client, receive_id_type="user_id", receive_id=user_id, msg_type="text",
                                       content="{\"text\":\"all files output\"}")
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
                create_message_request_wrapper(client, receive_id_type="user_id", receive_id=user_id, msg_type="file",
                                               content=content)
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
        content=get_card_source_string()
    )
    # patch_message_request_wrapper(client)


cards_map = {}


def update_card(body):
    app_id = 'cli_a5bb0a8ac8f99013'
    app_secret = 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.ERROR) \
        .build()

    action = body['action']
    tag = action['tag']
    open_message_id = body['open_message_id']
    user_id = body['user_id']
    if tag == 'button':
        record = cards_map[open_message_id]
        mapped_category, mapped_section, mapped_relationship = (
            record.get('category', '_'), record.get('section', '_'), record.get('relation', '_'))
        document_number = get_next_document_number(mapped_category, mapped_section, mapped_relationship)
        create_message_request_wrapper(
            client, receive_id_type="user_id", receive_id=user_id, msg_type="text",
            content="\{\"text\":\"%s\"\}" % (
                Document.print_code(
                    mapped_category, mapped_section, mapped_relationship, document_number
                )
            )
        )
    elif tag == 'select_static':
        key = action['value']['key']
        value = action['option']
        record = cards_map.get(open_message_id, {})
        record[key] = value
        cards_map[open_message_id] = record


# 调用
def main():
    output_wrapper("92e9d9e9")  # send to me


if __name__ == "__main__":
    main()
