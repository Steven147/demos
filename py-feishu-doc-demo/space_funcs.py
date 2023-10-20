import lark_oapi as lark
from lark_oapi.api.wiki.v2 import *


def list_space_request_wrapper(client):
    # 构造请求对象
    request: ListSpaceRequest = ListSpaceRequest.builder() \
        .build()

    # 发起请求
    response: ListSpaceResponse = client.wiki.v2.space.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def get_space_request_wrapper(client, space_id: str):
    # 构造请求对象
    request: GetSpaceRequest = GetSpaceRequest.builder() \
        .space_id(space_id) \
        .build()

    # 发起请求
    response: GetSpaceResponse = client.wiki.v2.space.get(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def list_space_node_request_wrapper(client, space_id: str, parent_node_token: str = ""):
    # 构造请求对象
    request: ListSpaceNodeRequest = ListSpaceNodeRequest.builder() \
        .space_id(space_id) \
        .parent_node_token(parent_node_token) \
        .build()

    # 发起请求
    response: ListSpaceNodeResponse = client.wiki.v2.space_node.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

def move_docs_to_wiki_space_node_request_wrapper(client, space_id: int, parent_wiki_token: str, obj_token: str):
    # 构造请求对象
    request: MoveDocsToWikiSpaceNodeRequest = MoveDocsToWikiSpaceNodeRequest.builder() \
        .space_id(space_id) \
        .request_body(MoveDocsToWikiSpaceNodeRequestBody.builder()
            .parent_wiki_token(parent_wiki_token)
            .obj_type("docx")
            .obj_token(obj_token)
            .build()) \
        .build()

    # 发起请求
    response: MoveDocsToWikiSpaceNodeResponse = client.wiki.v2.space_node.move_docs_to_wiki(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.move_docs_to_wiki failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))




