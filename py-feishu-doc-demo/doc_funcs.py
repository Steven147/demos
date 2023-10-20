import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
from lark_oapi.api.drive.v1 import *
from typing import Union
import os

def create_document_request_wrapper(client, folder_token: str, title: str = ""):

    # 构造请求对象
    request: CreateDocumentRequest = CreateDocumentRequest.builder() \
        .request_body(CreateDocumentRequestBody.builder()
            .folder_token(folder_token)
            .title(title)
            .build()) \
        .build()

    # 发起请求
    response: CreateDocumentResponse = client.docx.v1.document.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    
def create_export_task_request_wrapper(client, ext: str, token: str, type: str) -> Union[str, None]:

    # 构造请求对象
    request: CreateExportTaskRequest = CreateExportTaskRequest.builder() \
        .request_body(ExportTask.builder()
            .file_extension(ext)
            .token(token)
            .type(type)
            .build()) \
        .build()

    # 发起请求
    response: CreateExportTaskResponse = client.drive.v1.export_task.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.export_task.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    if (response.data != None):
        return response.data.ticket

def get_export_task_request_wrapper(client, ticket: str, token: str) -> Union[str, None]:
    # 构造请求对象
    request: GetExportTaskRequest = GetExportTaskRequest.builder() \
        .ticket(ticket) \
        .token(token) \
        .build()

    # 发起请求
    response: GetExportTaskResponse = client.drive.v1.export_task.get(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.export_task.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    if (response.data != None and response.data.result != None):
        return response.data.result.file_token


def download_export_task_request_wrapper(client, file_token: str):
    # 构造请求对象
    request: DownloadExportTaskRequest = DownloadExportTaskRequest.builder() \
        .file_token(file_token) \
        .build()

    # 发起请求
    response: DownloadExportTaskResponse = client.drive.v1.export_task.download(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.export_task.download failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    
    dir_path = os.path.dirname(__file__)  # 获取文件所在目录路径
    rel_path = os.path.join(dir_path, f"{response.file_name}")
    f = open(rel_path, "wb")
    if (response.file != None):
        f.write(response.file.read())
    f.close()
