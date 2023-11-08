# -*- coding: utf-8 -*-
import lark_oapi as lark
import os
import threading

from lark_oapi import Card

from source_request_funcs import (
    create_export_task_request_wrapper,
    get_export_task_request_wrapper,
    download_export_task_request_wrapper,
    create_wiki_document_request_wrapper, create_message_request_wrapper, list_space_node_request_wrapper,
    create_file_request_wrapper, create_document_block_children_request_wrapper
)
from source_watermark_funcs import trans_to_watermark_file
from source_database_funcs import get_card_source_string, get_next_document_number, Document, set_manual_record, \
    Mappings, find_manual_record, set_new_doc, get_code_title_list, find_all_records, map_manual_input
import time

app_id = 'cli_a5bb0a8ac8f99013'
app_secret = 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'
space_id = "7291489975366270978"
root_dir = os.path.dirname(__file__)
input_dir = os.path.join(root_dir, 'input_file')
output_dir = os.path.join(root_dir, 'output_file')  # 新建文件路径指向 output 文件夹
# 创建client
client = lark.Client.builder() \
    .app_id(app_id) \
    .app_secret(app_secret) \
    .log_level(lark.LogLevel.ERROR) \
    .build()

card_prefix = "卡片"
new_doc_prefix = "编码："
search_doc_prefix = "查询："
output_doc_prefix = "导出："
multi_search_doc_prefix = "批量查询："
multi_output_doc_prefix = "批量导出："
wiki_link_prefix = 'https://h4c12uuoah.feishu.cn/wiki/'

classmap = {
    '网络七期': 'VwrUwqamZiGRpGkndmGcFBJhn2d',
    '未来八期': 'LU46wq2kIixvGVkfenqcX4bMnfc'
}


# todo 改为异步获取
def export_file(client, token):
    attempts = 0  # 初始化轮询计数器
    max_attempts = 5
    interval = 1

    ticket = create_export_task_request_wrapper(client, ext="pdf", token=token, type='docx')
    if ticket is None:
        return

    file_token = None  # 初始化最后一次轮询的结果
    while attempts < max_attempts:
        file_token = get_export_task_request_wrapper(client, ticket, token)
        if file_token: break
        attempts += 1  # 增加轮询计数器
        time.sleep(interval * attempts)  # 添加轮询间隔等待时间

    if file_token:
        download_export_task_request_wrapper(client, file_token, output_dir='input_file')


def send_doc_guide(chat_id: str):
    send_doc_guide_inner(chat_id, 'chat_id', 'default')


def send_menu_doc_guide(user_id: str, key: str):
    send_doc_guide_inner(user_id, 'user_id', key)


def send_doc_guide_inner(receive_id: str, receive_id_type: str, key: str):
    guide_str_1_new_doc = (
        f"1. 分别输入文档信息，生成编码。\\n"
        f"-{Mappings.get_option_suggest('category')}\\n"
        f"-{Mappings.get_option_suggest('section')}\\n"
        f"-{Mappings.get_option_suggest('relationship')}\\n"
        f"-{Mappings.get_option_suggest('class_name')}\\n"
        f"-请输入标题:\\n"
        f"例如发送消息\\n"
        f"<<<{new_doc_prefix}秘笈、爱未来、生命成长类、未来八期、中国当代青年的样子\\n"
        f"自动回复\\n"
        f">>>生成编码和标题：A0403001中国当代青年的样子\\n"
        f">>>生成知识库链接：... \\n"
        f"\\n"
    )
    guide_str_2_search_doc = (
        f"2.1 输入编码，查询文章\\n"
        f"例如发送消息\\n"
        f"<<<{search_doc_prefix}A0403001\\n"
        f"自动回复文档查询结果\\n"
        f">>>查询到的编码和标题：A0403001中国当代青年的样子\\n"
        f">>>查询到的知识库链接：... \\n"
        f"2.2 输入课程，查询所有文章\\n"
        f"-{Mappings.get_option_suggest('class_name')}\\n"
        f"例如发送消息\\n"
        f"<<<{multi_search_doc_prefix}未来八期\\n"
        f"会自动回复课程内的所有文档结果\\n"
        f"\\n"
    )
    guide_str_3_output_doc = (
        f"3.1 输入编码，导出文档\\n"
        f"例如发送消息\\n"
        f"<<<{output_doc_prefix}A0403001\\n"
        f"自动回复文档文件\\n"
        f">>>[A0403001中国当代青年的样子.pdf]\\n"
        f"3.2 输入课程名，导出所有文档\\n"
        f"例如发送消息\\n"
        f"<<<{multi_output_doc_prefix}未来八期\\n"
        f"会自动回复课程内的所有文档文件\\n"
    )
    guide_str = (
        f"命令帮助\\n"
    )

    if key == 'menu0201' or key == 'default':
        guide_str += (guide_str_1_new_doc + guide_str_2_search_doc + guide_str_3_output_doc)
    elif key == 'menu0202':
        guide_str += guide_str_1_new_doc
    elif key == 'menu0203':
        guide_str += guide_str_2_search_doc
    elif key == 'menu0204':
        guide_str += guide_str_3_output_doc
    else:
        return

    create_message_request_wrapper(
        client,
        receive_id_type=receive_id_type,
        receive_id=receive_id,
        msg_type="text",
        content="{\"text\":\"" + guide_str + "\"}"
    )


def is_help_text(text: str):
    for keywords in ['help', '帮助']:
        if text.find(keywords) >= 0:
            return True
    return False


def output_export_func_inner(doc: Document, chat_id: str):
    if not doc:
        create_message_request_wrapper(
            client,
            receive_id_type="chat_id",
            receive_id=chat_id,
            msg_type="text",
            content="{\"text\":\"找不到对应文档\"}"
        )
    else:
        export_file(client, doc.obj_token)


def output_upload_func_inner(doc: Document, chat_id: str):
    trans_to_watermark_file(
        name='爱与幸福文字中心',
        input_dir=input_dir,
        output_dir=output_dir,
        new_watermark=True
    )
    file_name = f"{str(doc.get_code_title())}.pdf"
    file_key = create_file_request_wrapper(client, file_name, os.path.join(output_dir, file_name))
    content = "{\"file_key\":\"%s\"}" % file_key
    create_message_request_wrapper(
        client, receive_id_type="chat_id", receive_id=chat_id, msg_type="file",
        content=content
    )


def output_func(message_str: str, chat_id: str):
    doc = find_manual_record(message_str.removeprefix(output_doc_prefix))
    output_export_func_inner(doc, chat_id)
    output_upload_func_inner(doc, chat_id)


def multi_output_func(message_str: str, chat_id: str):
    docs = find_all_records(message_str.removeprefix(multi_output_doc_prefix))
    # 创建一个线程列表来保存所有新创建的线程
    threads = []

    # 创建一个新的线程来运行output_func_inner函数
    for doc in docs:
        thread = threading.Thread(target=output_export_func_inner, args=(doc, chat_id))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    for doc in docs:
        output_upload_func_inner(doc, chat_id)


def search_code_func(message_str: str, chat_id: str):
    doc = find_manual_record(message_str.removeprefix(search_doc_prefix))
    if not doc:
        create_message_request_wrapper(
            client,
            receive_id_type="chat_id",
            receive_id=chat_id,
            msg_type="text",
            content="{\"text\":\"找不到对应文档\"}"
        )
    else:
        response_text = (f"查询到的编码和标题：{str(doc.get_code_title())} \\n"
                         f"查询到的知识库链接：{wiki_link_prefix}{str(doc.token)}")
        # todo 新增文件更新与上传
        create_message_request_wrapper(
            client,
            receive_id_type="chat_id",
            receive_id=chat_id,
            msg_type="text",
            content="{\"text\":\"" + response_text + "\"}"
        )


def multi_search_code_func(message_str: str, chat_id: str):
    docs = find_all_records(message_str.removeprefix(multi_search_doc_prefix))
    response_text = ""
    for doc in docs:
        response_text = (f"{response_text}"
                         f"查询到的编码和标题：{str(doc.get_code_title())}\\n"
                         f"查询到的知识库链接：{wiki_link_prefix}{str(doc.token)}\\n\\n")
    create_message_request_wrapper(
        client,
        receive_id_type="chat_id",
        receive_id=chat_id,
        msg_type="text",
        content="{\"text\":\"" + response_text + "\"}"
    )


def new_code_params(message_str: str, chat_id: str):
    new_doc = set_manual_record(
        *map_manual_input(message_str.removeprefix(new_doc_prefix))
    )  # without token and obj token when callback
    new_file(new_doc, chat_id)


def new_file(new_doc: Document, chat_id: str):
    new_code_title = new_doc.get_code_title()
    new_parent_node = new_doc.parent_token
    # 【文档】“我们是中国的未来”孝亲反哺专场第8期 https://h4c12uuoah.feishu.cn/wiki/LU46wq2kIixvGVkfenqcX4bMnfc

    node = create_wiki_document_request_wrapper(client, space_id, new_parent_node, new_code_title)
    create_document_block_children_request_wrapper(
        client, node.obj_token, node.obj_token, new_doc.get_sub_title()
    )
    document_link = f"{wiki_link_prefix}{str(node.node_token)}"
    new_doc.token = node.node_token
    new_doc.obj_token = node.obj_token
    Document.commit_session()

    # todo 新增上下标自动更新
    response_text = (f"生成编码和标题：{str(new_code_title)} \\n"
                     f"生成知识库链接：{document_link}")

    create_message_request_wrapper(
        client,
        receive_id_type="chat_id",
        receive_id=chat_id,
        msg_type="text",
        content="{\"text\":\"" + response_text + "\"}"
    )


#
# def output_wrapper(user_id: str):
#     need_update = True
#     need_upload = True
#     space_id = '7291489975366270978'
#     parent_node = 'LU46wq2kIixvGVkfenqcX4bMnfc'  # 【文档】“我们是中国的未来”孝亲反哺专场第8期
#     obj_token = "FgBmdX4YioQsacxNkpUcMiUmnmh"
#     # "space_id": "7291489975366270978",
#     # "node_token": "LU46wq2kIixvGVkfenqcX4bMnfc",
#     # "obj_token": "FgBmdX4YioQsacxNkpUcMiUmnmh",
#
#     # list_space_request_wrapper(client)
#     # get_space_request_wrapper(client, '7291489975366270978')
#     # list_space_node_request_wrapper(client, '7291489975366270978')  root node
#     # list_space_node_request_wrapper(client, '7291489975366270978', 'OEecwNC8nipwKekmM1wcJRgZno9') # 首页 node
#     # list_space_node_request_wrapper(client, '7291489975366270978', 'P3m9wICTii7egIkB9vLcEnkPnic') # 遍历 芳芳老师文档整理
#     # create_document_request_wrapper(client, "", "new doc")
#
#     # move_docs_to_wiki_space_node_request_wrapper(client, 7291489975366270978, 'LU46wq2kIixvGVkfenqcX4bMnfc',
#     # obj_token= 'EW9LdimcWodD6NxOUgHcOTi2nOb')
#
#     create_message_request_wrapper(client, receive_id_type="user_id", receive_id=user_id, msg_type="text",
#                                    content="{\"text\":\"processing...\"}")
#     if need_update:
#         nodes = list_space_node_request_wrapper(client, space_id, parent_node)  # 遍历
#         if nodes:
#             for node in nodes:
#                 export_file(client, node.obj_token)
#
#         trans_to_watermark_file(
#             name='爱与幸福文字中心',
#             input_dir=input_dir,
#             output_dir=output_dir,
#         )
#
#     if need_upload:
#         create_message_request_wrapper(client, receive_id_type="user_id", receive_id=user_id, msg_type="text",
#                                        content="{\"text\":\"all files output\"}")
#         for dir_path, dirnames, file_names in os.walk(output_dir):
#             for file_name in sorted(file_names):
#                 # file_token = upload_all_media_request_wrapper(
#                 #         client=client,
#                 #         file_name=file_name,
#                 #         file_path=file_path,
#                 #         parent_type='docx_file',
#                 #         parent_node=obj_token
#                 #     )
#                 # block_id = create_document_block_children_request_wrapper(client, document_id=obj_token, block_id=obj_token)
#                 # patch_document_block_request_wrapper(client, document_id=obj_token, block_id=block_id, file_token=file_token)
#                 # file_tokens.append(file_token)
#
#                 file_key = create_file_request_wrapper(client, file_name, os.path.join(dir_path, file_name))
#                 content = "{\"file_key\":\"%s\"}" % file_key
#                 create_message_request_wrapper(client, receive_id_type="user_id", receive_id=user_id, msg_type="file",
#                                                content=content)
#                 # create_message_request_wrapper(client, receive_id_type="user_id",receive_id="ca4ba8a3", msg_type="file", content=content)
#                 # ca4ba8a3
#
#     # for file_token in file_tokens:
#
#     # patch_document_block_request_wrapper(client, document_id=obj_token, block_id=block_id, file_token=file_token)


def send_card(receive_id_type: str, receive_id: str):
    create_message_request_wrapper(
        client,
        receive_id_type=receive_id_type,
        receive_id=receive_id,
        msg_type="interactive",
        content=get_card_source_string()
    )
    # patch_message_request_wrapper(client)


cards_map = {}


def card_action(card: Card):
    action = card.action
    tag = action.tag
    open_message_id = card.open_message_id
    open_chat_id = card.open_chat_id
    if tag == 'button':
        record = cards_map[open_message_id]
        mapped_category, mapped_section, mapped_relationship, mapped_parent_token = (
            record.get('category'), record.get('section'), record.get('relationship'), record.get('class_name')
        )
        if mapped_category is None or mapped_section is None or mapped_relationship is None or mapped_parent_token is None:
            lark.logger.error("[update_card] button press without enough key" + str(cards_map))
            return
        new_file(
            set_manual_record(mapped_category, mapped_section, mapped_relationship, mapped_parent_token, ""),
            open_chat_id,
        )
    elif tag == 'select_static':
        key = action.value["key"]
        value = action.option
        record = cards_map.get(open_message_id, {})
        record[key] = value
        lark.logger.info(f"[update_card] select key {key}, value {value}")
        cards_map[open_message_id] = record


def update_card(body):
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
                Document.get_code(mapped_category, mapped_section, mapped_relationship, document_number)
            )
        )
    elif tag == 'select_static':
        key = action['value']['key']
        value = action['option']
        record = cards_map.get(open_message_id, {})
        record[key] = value
        cards_map[open_message_id] = record


# 根据wiki response数据，新建数据库记录
def new_db_record(message_str: str, parent_node_token: str, node_token: str, obj_token: str):
    mapped_category, mapped_section, mapped_relationship, document_number, title = get_code_title_list(message_str)
    set_new_doc(
        mapped_category, mapped_section, mapped_relationship, document_number, title,
        node_token, obj_token, parent_node_token
    )


# 调用
def sync_db_with_wiki():
    # output_wrapper("92e9d9e9")  # send to me
    # todo 手动删除数据库
    space_id = '7291489975366270978'
    parent_nodes = ['LU46wq2kIixvGVkfenqcX4bMnfc', 'VwrUwqamZiGRpGkndmGcFBJhn2d']  # 【文档】“我们是中国的未来”孝亲反哺专场第8期

    for parent_node in parent_nodes:
        nodes = list_space_node_request_wrapper(client, space_id, parent_node)  # 遍历
        for node in nodes:
            new_db_record(node.title, node.parent_node_token, node.node_token, node.obj_token)


if __name__ == "__main__":
    sync_db_with_wiki()  # 直接在文档中更新数据库后，需要reset