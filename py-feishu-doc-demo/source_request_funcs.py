import lark_oapi as lark
import lark_oapi.api.docx.v1 as docxV1
import lark_oapi.api.drive.v1 as driveV1
import lark_oapi.api.wiki.v2 as wikiV2
import lark_oapi.api.im.v1 as imV1
from typing import Optional
from lark_oapi.client import Client
import os

# 创建client
client = lark.Client.builder() \
    .app_id('cli_a5bb0a8ac8f99013') \
    .app_secret('rceFwGZuDFcP1fYwjc812ftAsysPK1MZ') \
    .log_level(lark.LogLevel.ERROR) \
    .build()

def list_space_request_wrapper():
    # 构造请求对象
    request: wikiV2.ListSpaceRequest = wikiV2.ListSpaceRequest.builder() \
        .build()

    # 发起请求
    response: wikiV2.ListSpaceResponse = client.wiki.v2.space.list(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def get_space_request_wrapper(space_id: str):
    # 构造请求对象
    # pyright: ignore[reportGeneralTypeIssues]
    request: wikiV2.GetSpaceRequest = wikiV2.GetSpaceRequest.builder() \
        .space_id(space_id) \
        .build()

    # 发起请求

    response: wikiV2.GetSpaceResponse = client.wiki.v2.space.get(request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def list_space_node_request_wrapper(space_id: str, parent_node_token: str = "") -> Optional[
    wikiV2.List[wikiV2.Node]]:
    # 构造请求对象
    request: wikiV2.ListSpaceNodeRequest = wikiV2.ListSpaceNodeRequest.builder() \
        .space_id(space_id) \
        .parent_node_token(parent_node_token) \
        .build()

    # 发起请求
    response: wikiV2.ListSpaceNodeResponse = client.wiki.v2.space_node.list(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data.items  # pyright: ignore[reportOptionalMemberAccess]


def move_docs_to_wiki_space_node_request_wrapper(space_id: int, parent_wiki_token: str, obj_token: str):
    # 构造请求对象
    request: wikiV2.MoveDocsToWikiSpaceNodeRequest = wikiV2.MoveDocsToWikiSpaceNodeRequest.builder() \
        .space_id(space_id) \
        .request_body(wikiV2.MoveDocsToWikiSpaceNodeRequestBody.builder()
                      .parent_wiki_token(parent_wiki_token)
                      .obj_type("docx")
                      .obj_token(obj_token)
                      .build()) \
        .build()

    # 发起请求
    response: wikiV2.MoveDocsToWikiSpaceNodeResponse = client.wiki.v2.space_node.move_docs_to_wiki(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.move_docs_to_wiki failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def upload_all_media_request_wrapper(file_name: str, file_path: str, parent_type: str,
                                     parent_node: str) -> Optional[str]:
    # 构造请求对象
    request: driveV1.UploadAllMediaRequest = driveV1.UploadAllMediaRequest.builder() \
        .request_body(driveV1.UploadAllMediaRequestBody.builder()
                      .file_name(file_name)
                      .parent_type(parent_type)
                      .parent_node(parent_node)
                      .size(os.path.getsize(file_path))
                      .file((open(file_path, 'rb')))
                      .build()) \
        .build()

    # 发起请求
    response: driveV1.UploadAllMediaResponse = client.drive.v1.media.upload_all(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.media.upload_all failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data.file_token  # pyright: ignore[reportOptionalMemberAccess]


def create_document_request_wrapper(folder_token: str, title: str = ""):
    # 构造请求对象
    request: docxV1.CreateDocumentRequest = docxV1.CreateDocumentRequest.builder() \
        .request_body(docxV1.CreateDocumentRequestBody.builder()
                      .folder_token(folder_token)
                      .title(title)
                      .build()) \
        .build()

    # 发起请求
    response: docxV1.CreateDocumentResponse = client.docx.v1.document.create(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def create_export_task_request_wrapper(ext: str, token: str, type: str) -> Optional[str]:
    # 构造请求对象
    request: driveV1.CreateExportTaskRequest = driveV1.CreateExportTaskRequest.builder() \
        .request_body(driveV1.ExportTask.builder()
                      .file_extension(ext)
                      .token(token)
                      .type(type)
                      .build()) \
        .build()

    # 发起请求
    response: driveV1.CreateExportTaskResponse = client.drive.v1.export_task.create(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.export_task.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    if (response.data != None):
        return response.data.ticket


def get_export_task_request_wrapper(ticket: str, token: str) -> Optional[str]:
    # 构造请求对象
    request: driveV1.GetExportTaskRequest = driveV1.GetExportTaskRequest.builder() \
        .ticket(ticket) \
        .token(token) \
        .build()

    # 发起请求
    response: driveV1.GetExportTaskResponse = client.drive.v1.export_task.get(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.export_task.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    if (response.data != None and response.data.result != None):
        return response.data.result.file_token


def download_export_task_request_wrapper(file_token: str, output_dir):
    # 构造请求对象
    request: driveV1.DownloadExportTaskRequest = driveV1.DownloadExportTaskRequest.builder() \
        .file_token(file_token) \
        .build()

    # 发起请求
    response: driveV1.DownloadExportTaskResponse = client.drive.v1.export_task.download(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.export_task.download failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.file_name, indent=4))
    dir_path = os.path.dirname(__file__)  # 获取文件所在目录路径
    os.makedirs(os.path.join(dir_path, output_dir), exist_ok=True)  # 创建 output 文件夹，如果已存在则不会报错
    rel_path = os.path.join(dir_path, output_dir, f"{response.file_name}")  # 新建文件路径指向 output 文件夹
    f = open(rel_path, "wb")
    if (response.file != None):
        f.write(response.file.read())
    f.close()


def create_document_block_children_request_wrapper(
         document_id: str, block_id: str, text: str
) -> Optional[str]:

    body = docxV1.CreateDocumentBlockChildrenRequestBody.builder()\
            .children([docxV1.Block.builder() \
                .block_type(2)
                .text(docxV1.Text.builder()
                    .style(docxV1.TextStyle.builder()
                        .build())
                    .elements([docxV1.TextElement.builder()
                        .text_run(docxV1.TextRun.builder()
                            .content(text)
                            .text_element_style(docxV1.TextElementStyle.builder()
                                .bold(True)
                                .build())
                            .build())
                        .build()
                        ])
                    .build())
                .build()
                ]) \
            .index(0) \
            .build()

    # 构造请求对象
    request: docxV1.CreateDocumentBlockChildrenRequest = docxV1.CreateDocumentBlockChildrenRequest.builder() \
        .document_id(document_id) \
        .block_id(block_id) \
        .document_revision_id(-1) \
        .request_body(body) \
        .build()

    # 发起请求
    response: docxV1.CreateDocumentBlockChildrenResponse = client.docx.v1.document_block_children.create(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document_block_children.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data.children[0].block_id  # pyright: ignore[reportOptionalSubscript, reportOptionalMemberAccess]


def patch_document_block_request_wrapper(document_id: str, block_id: str, file_token: str):
    # 构造请求对象
    request: docxV1.PatchDocumentBlockRequest = docxV1.PatchDocumentBlockRequest.builder() \
        .document_id(document_id) \
        .block_id(block_id) \
        .request_body(docxV1.UpdateBlockRequest.builder()
                      .replace_file(docxV1.ReplaceFileRequest.builder()
                                    .token(file_token)
                                    .build())
                      .build()) \
        .build()

    # 发起请求
    response: docxV1.PatchDocumentBlockResponse = client.docx.v1.document_block.patch(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document_block.patch failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def create_file_request_wrapper(file_name: str, file_path: str) -> Optional[str]:
    # 构造请求对象
    request: imV1.CreateFileRequest = imV1.CreateFileRequest.builder() \
        .request_body(imV1.CreateFileRequestBody.builder()
                      .file_type("pdf")
                      .file_name(file_name)
                      .file((open(file_path, 'rb')))
                      .build()) \
        .build()

    # 发起请求
    response: imV1.CreateFileResponse = client.im.v1.file.create(request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.file.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data.file_key  # pyright: ignore[reportOptionalMemberAccess]


def create_message_request_wrapper(receive_id_type: str, receive_id: str, msg_type: str, content: str):
    # 构造请求对象
    request: imV1.CreateMessageRequest = imV1.CreateMessageRequest.builder() \
        .receive_id_type(receive_id_type) \
        .request_body(imV1.CreateMessageRequestBody.builder()
                      .receive_id(receive_id)
                      .msg_type(msg_type)
                      .content(content)
                      .build()) \
        .build()

    # 发起请求
    response: imV1.CreateMessageResponse = client.im.v1.message.create(
        request)  # pyright: ignore[reportOptionalMemberAccess]

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def patch_message_request_wrapper( message_id: str, content: str):
    # 构造请求对象
    request: imV1.PatchMessageRequest = imV1.PatchMessageRequest.builder() \
        .message_id(message_id) \
        .request_body(imV1.PatchMessageRequestBody.builder()
                      .content(content)
                      .build()) \
        .build()

    # 发起请求
    response: imV1.PatchMessageResponse = client.im.v1.message.patch(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.patch failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return


def create_wiki_document_request_wrapper(space_id: str, folder_token: str, title: str):
    # 构造请求对象
    request: wikiV2.CreateSpaceNodeRequest = wikiV2.CreateSpaceNodeRequest.builder() \
        .space_id(space_id) \
        .request_body(wikiV2.Node.builder()
                      .obj_type("docx")
                      .parent_node_token(folder_token)
                      .node_type("origin")
                      .origin_node_token("")
                      .title(title)
                      .build()) \
        .build()

    # 发起请求
    response: wikiV2.CreateSpaceNodeResponse = client.wiki.v2.space_node.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.create, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data.node
