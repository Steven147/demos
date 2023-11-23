import asyncio

from lark_oapi.api.application.v6 import P2ApplicationBotMenuV6

from model.card_model import CardModel
from model.client_model import ClientModel
from model.files_model.files_model import FilesModel
import time
import os
import lark_oapi as lark
import threading
import json
import lark_oapi.api.im.v1 as imV1

from lark_oapi import Card

from model.source_database_funcs import get_card_source_string, get_next_document_number, Document, \
    Mappings, find_manual_record, get_code_title_list, find_all_records, map_manual_input


class Command:
    sync_db_prefix = "同步"
    card_prefix = "卡片"
    new_doc_prefix = "编码："
    search_doc_prefix = "查询："
    output_doc_prefix = "导出："
    multi_search_doc_prefix = "批量查询："
    multi_output_doc_prefix = "批量导出："
    wiki_link_prefix = 'https://h4c12uuoah.feishu.cn/wiki/'


class TaskController:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_thread_loop).start()

    def start_thread_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()


class SpaceTaskController(TaskController):
    def __init__(self, space_id: str):
        super().__init__()
        self.space_id = space_id
        self.card_model = CardModel()
        self.cards_map = {}
        self.files_model = FilesModel()
        self.client_model = ClientModel(
            'cli_a5bb0a8ac8f99013', 'rceFwGZuDFcP1fYwjc812ftAsysPK1MZ'
        )

    # 如果您的应用并不需要实时与用户交互结果，可以将这些任务与 HTTP 处理逻辑分离，交给另一个专注于后台任务处理的服务（如 Celery）。
    # 这样就可以使得 Web 服务器专注于它最擅长的事情——处理尽可能多的 HTTP 请求，而不必为那些可异步处理的耗时任务而等待。

    # 正常情况下，使用asyncio调用run，只是运行了事件循环，但flask不支持，也就等价于同步。
    # 因此，还是需要采用asyncio.new_event_loop的方式，将接下来的处理交给事件循环。然后直接返回response。

    def card_action(self, card: Card):
        self.loop.call_soon_threadsafe(self._card_action, card)

    def im_message_receive(self, data: imV1.P2ImMessageReceiveV1):
        self.loop.call_soon_threadsafe(self._im_message_receive, data)

    def bot_menu(self, data: P2ApplicationBotMenuV6):
        self.loop.call_soon_threadsafe(self._bot_menu, data)

    def _card_action(self, card: Card):
        action = card.action
        tag = action.tag
        open_message_id = card.open_message_id
        open_chat_id = card.open_chat_id
        if tag == 'button':
            record = self.cards_map[open_message_id]
            mapped_category, mapped_section, mapped_relationship, mapped_parent_token = (
                record.get('category'), record.get('section'), record.get('relationship'), record.get('class_name')
            )
            if (mapped_category is None or mapped_section is None
                    or mapped_relationship is None or mapped_parent_token is None):
                lark.logger.error("[update_card] button press without enough key" + str(self.cards_map))
                return
            self._create_record_and_doc(
                mapped_category, mapped_section, mapped_relationship, mapped_parent_token, open_chat_id, title=""
            )
        elif tag == 'select_static':
            key = action.value["key"]
            value = action.option
            record = self.cards_map.get(open_message_id, {})
            record[key] = value
            lark.logger.info(f"[update_card] select key {key}, value {value}")
            self.cards_map[open_message_id] = record

    def _im_message_receive(self, data: imV1.P2ImMessageReceiveV1):
        ctt = json.loads(data.event.message.content)
        chat_id = data.event.message.chat_id
        content = ctt['text']
        if self._is_help_text(content):
            self._send_doc_guide(chat_id)
        elif content.startswith(Command.sync_db_prefix):
            self._sync_db_with_wiki()
        elif content.startswith(Command.card_prefix):
            self._send_card("chat_id", chat_id)
        elif content.startswith(Command.new_doc_prefix):
            self._new_doc_func(content, chat_id)
        elif content.startswith(Command.search_doc_prefix):
            self._search_code_func(content, chat_id)
        elif content.startswith(Command.multi_search_doc_prefix):
            self._multi_search_code_func(content, chat_id)
        elif content.startswith(Command.output_doc_prefix):
            self._output_func(content, chat_id)
        elif content.startswith(Command.multi_output_doc_prefix):
            self._multi_output_func(content, chat_id)

    def _bot_menu(self, data: P2ApplicationBotMenuV6):
        key = data.event.event_key
        user_id = data.event.operator.operator_id.user_id
        self._send_menu_doc_guide(user_id, key)

    def _send_doc_guide(self, chat_id: str):
        self._send_doc_guide_inner(chat_id, 'chat_id', 'default')

    def _send_menu_doc_guide(self, user_id: str, key: str):
        self._send_doc_guide_inner(user_id, 'user_id', key)

    def _is_help_text(self, text: str):
        for keywords in ['help', '帮助']:
            if text.find(keywords) >= 0:
                return True
        return False

    def _output_func(self, message_str: str, chat_id: str):
        doc = self._get_single_record_inner(message_str, Command.output_doc_prefix)
        self._output_export_func_inner(doc, chat_id)
        self._output_upload_func_inner(doc, chat_id)

    def _multi_output_func(self, message_str: str, chat_id: str):
        docs = find_all_records(message_str.removeprefix(Command.multi_output_doc_prefix))
        # 创建一个线程列表来保存所有新创建的线程
        threads = []

        # 创建一个新的线程来运行output_func_inner函数
        for doc in docs:
            thread = threading.Thread(target=self._output_export_func_inner, args=(doc, chat_id))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        for doc in docs:
            self._output_upload_func_inner(doc, chat_id)

    def _search_code_func(self, message_str: str, chat_id: str):
        doc = self._get_single_record_inner(message_str, Command.search_doc_prefix)
        if not doc:
            self.client_model.create_message_request_wrapper(receive_id_type="chat_id", receive_id=chat_id,
                                                             msg_type="text",
                                                             content="{\"text\":\"找不到对应文档\"}")
        else:
            response_text = (f"查询到的编码和标题：{str(doc.get_code_title())} \\n"
                             f"查询到的知识库链接：{Command.wiki_link_prefix}{str(doc.token)}")
            self.client_model.create_message_request_wrapper(receive_id_type="chat_id", receive_id=chat_id,
                                                             msg_type="text",
                                                             content="{\"text\":\"" + response_text + "\"}")

    def _multi_search_code_func(self, message_str: str, chat_id: str):
        docs = find_all_records(message_str.removeprefix(Command.multi_search_doc_prefix))
        response_text = ""
        for doc in docs:
            response_text = (f"{response_text}"
                             f"查询到的编码和标题：{str(doc.get_code_title())}\\n"
                             f"查询到的知识库链接：{Command.wiki_link_prefix}{str(doc.token)}\\n\\n")
        self.client_model.create_message_request_wrapper(receive_id_type="chat_id", receive_id=chat_id, msg_type="text",
                                                         content="{\"text\":\"" + response_text + "\"}")

    def _new_doc_func(self, message_str: str, chat_id: str):
        mapped_category, mapped_section, mapped_relationship, mapped_parent_token, title \
            = map_manual_input(message_str.removeprefix(Command.new_doc_prefix))
        self._create_record_and_doc(mapped_category, mapped_section, mapped_relationship, mapped_parent_token, chat_id,
                                    title)

    # def update_card(body):
    #     action = body['action']
    #     tag = action['tag']
    #     open_message_id = body['open_message_id']
    #     user_id = body['user_id']
    #     if tag == 'button':
    #         record = cards_map[open_message_id]
    #         mapped_category, mapped_section, mapped_relationship = (
    #             record.get('category', '_'), record.get('section', '_'), record.get('relation', '_'))
    #         document_number = get_next_document_number(mapped_category, mapped_section, mapped_relationship)
    #         create_message_request_wrapper(
    #             client, receive_id_type="user_id", receive_id=user_id, msg_type="text",
    #             content="\{\"text\":\"%s\"\}" % (
    #                 Document.get_code(mapped_category, mapped_section, mapped_relationship, document_number)
    #             )
    #         )
    #     elif tag == 'select_static':
    #         key = action['value']['key']
    #         value = action['option']
    #         record = cards_map.get(open_message_id, {})
    #         record[key] = value
    #         cards_map[open_message_id] = record

    def _send_card(self, receive_id_type: str, receive_id: str):
        self.client_model.create_message_request_wrapper(
            receive_id_type=receive_id_type, receive_id=receive_id, msg_type="interactive",
            content=get_card_source_string()
        )
        # patch_message_request_wrapper(client)

    def _send_doc_guide_inner(self, receive_id: str, receive_id_type: str, key: str):
        guide_str_1_new_doc = (
            f"1. 分别输入文档信息，生成编码。\\n"
            f"-{Mappings.get_option_suggest('category')}\\n"
            f"-{Mappings.get_option_suggest('section')}\\n"
            f"-{Mappings.get_option_suggest('relationship')}\\n"
            f"-{Mappings.get_option_suggest('class_name')}\\n"
            f"-请输入标题:\\n"
            f"例如发送消息\\n"
            f"<<<{Command.new_doc_prefix}秘笈、爱未来、生命成长类、未来八期、中国当代青年的样子\\n"
            f"自动回复\\n"
            f">>>生成编码和标题：A0403001中国当代青年的样子\\n"
            f">>>生成知识库链接：... \\n"
            f"\\n"
        )
        guide_str_2_search_doc = (
            f"2.1 输入编码，查询文章\\n"
            f"例如发送消息\\n"
            f"<<<{Command.search_doc_prefix}A0403001\\n"
            f"自动回复文档查询结果\\n"
            f">>>查询到的编码和标题：A0403001中国当代青年的样子\\n"
            f">>>查询到的知识库链接：... \\n"
            f"2.2 输入课程，查询所有文章\\n"
            f"-{Mappings.get_option_suggest('class_name')}\\n"
            f"例如发送消息\\n"
            f"<<<{Command.multi_search_doc_prefix}未来八期\\n"
            f"会自动回复课程内的所有文档结果\\n"
            f"\\n"
        )
        guide_str_3_output_doc = (
            f"3.1 输入编码，导出文档\\n"
            f"例如发送消息\\n"
            f"<<<{Command.output_doc_prefix}A0403001\\n"
            f"自动回复文档文件\\n"
            f">>>[A0403001中国当代青年的样子.pdf]\\n"
            f"3.2 输入课程名，导出所有文档\\n"
            f"例如发送消息\\n"
            f"<<<{Command.multi_output_doc_prefix}未来八期\\n"
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

        self.client_model.create_message_request_wrapper(receive_id_type=receive_id_type, receive_id=receive_id,
                                                         msg_type="text",
                                                         content="{\"text\":\"" + guide_str + "\"}")

    def _get_single_record_inner(self, message_str: str, prefix: str):
        mapped_category, mapped_section, mapped_relationship, document_number_str, _ = (
            get_code_title_list(
                message_str.removeprefix(prefix)
            )
        )
        return find_manual_record(mapped_category, mapped_section, mapped_relationship, document_number_str)

    def _create_record_and_doc(
            self, mapped_category: str, mapped_section: str, mapped_relationship: str, mapped_parent_token: str,
            chat_id: str,
            title: str = ''
    ):
        document_number = get_next_document_number(mapped_category, mapped_section, mapped_relationship)
        new_doc = Document(  # without token and obj token before callback
            category=mapped_category,
            section=mapped_section,
            relationship=mapped_relationship,
            document_number=document_number,
            parent_token=mapped_parent_token,
            title=title,
            token='',
            obj_token=''
        )
        # Document(
        #     category='mapped_category',
        #     section='mapped_section',
        #     relationship='mapped_relationship',
        #     document_number=1,
        #     parent_token='mapped_parent_token',
        #     title='title',
        #     token='',
        #     obj_token=''
        # )
        new_code_title = new_doc.get_code_title()
        new_parent_node = new_doc.parent_token
        # 【文档】“我们是中国的未来”孝亲反哺专场第8期 https://h4c12uuoah.feishu.cn/wiki/LU46wq2kIixvGVkfenqcX4bMnfc

        node = self.client_model.create_wiki_document_request_wrapper(self.space_id, new_parent_node, new_code_title)
        self.client_model.create_document_block_children_request_wrapper(
            node.obj_token,
            node.obj_token,
            new_doc.get_sub_title(),
            Mappings.get_class_fullname(new_parent_node),
            Mappings.get_timestamp_version()
        )
        document_link = f"{Command.wiki_link_prefix}{str(node.node_token)}"
        new_doc.token = node.node_token
        new_doc.obj_token = node.obj_token
        new_doc.commit_add_doc()

        # todo 新增上下标自动更新
        response_text = (f"生成编码和标题：{str(new_code_title)} \\n"
                         f"生成知识库链接：{document_link}")

        self.client_model.create_message_request_wrapper(receive_id_type="chat_id", receive_id=chat_id, msg_type="text",
                                                         content="{\"text\":\"" + response_text + "\"}")

    def _output_export_func_inner(self, doc: Document, chat_id: str):
        if not doc:
            self.client_model.create_message_request_wrapper(receive_id_type="chat_id", receive_id=chat_id,
                                                             msg_type="text",
                                                             content="{\"text\":\"找不到对应文档\"}")
        else:
            self._export_file(doc.obj_token)

    def _output_upload_func_inner(self, doc: Document, chat_id: str):
        self.files_model.trans_to_watermark_file(name='爱与幸福文字中心', new_watermark=True)
        file_name = f"{str(doc.get_code_title())}.pdf"
        file_key = self.client_model.create_file_request_wrapper(
            file_name, os.path.join(self.files_model.output_dir, file_name)
        )
        content = "{\"file_key\":\"%s\"}" % file_key
        self.client_model.create_message_request_wrapper(receive_id_type="chat_id", receive_id=chat_id, msg_type="file",
                                                         content=content)

    # todo 改为多线程获取
    def _export_file(self, token):
        attempts = 0  # 初始化轮询计数器
        max_attempts = 5
        interval = 1

        ticket = self.client_model.create_export_task_request_wrapper(ext="pdf", token=token, _type='docx')
        if ticket is None:
            return

        file_token = None  # 初始化最后一次轮询的结果
        while attempts < max_attempts:
            file_token = self.client_model.get_export_task_request_wrapper(ticket, token)
            if file_token:
                break
            attempts += 1  # 增加轮询计数器
            time.sleep(interval * attempts)  # 添加轮询间隔等待时间

        if file_token:
            self.client_model.download_export_task_request_wrapper(file_token, output_dir='../model/files_model/input_file')

    # 调用
    def _sync_db_with_wiki(self):
        Document.clear_database()
        parent_nodes = ['LU46wq2kIixvGVkfenqcX4bMnfc', 'VwrUwqamZiGRpGkndmGcFBJhn2d']  # 【文档】“我们是中国的未来”孝亲反哺专场第8期

        for parent_node in parent_nodes:
            nodes = self.client_model.list_space_node_request_wrapper(self.space_id, parent_node)  # 遍历
            for node in nodes:
                mapped_category, mapped_section, mapped_relationship, document_number, title = (
                    get_code_title_list(node.title)
                )
                Document(  # recreate document with all info
                    category=mapped_category,
                    section=mapped_section,
                    relationship=mapped_relationship,
                    document_number=int(document_number),
                    title=title,
                    token=node.node_token,
                    obj_token=node.obj_token,
                    parent_token=node.parent_node_token
                ).commit_add_doc()
