from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
      method=Method.PUT.value,
      path="/files",
      handler=handler.put_embed_files_handler,
      status_code=201
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/files",
      handler=handler.get_files_handler
    ),
    HandlerRequestType(
      method=Method.DELETE.value,
      path="/files",
      handler=handler.delete_file_handler
    ),
    HandlerRequestType(
      method=Method.DELETE.value,
      path="/files/knowledge",
      handler=handler.delete_file_handler
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/files/download/{file_id}",
      handler=handler.get_files_download_by_id_handler
    )
  ]