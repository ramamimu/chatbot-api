from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


def routes(handler) -> HandlerRequestType:
  return [
    HandlerRequestType(
      method=Method.PUT,
      path="/files",
      handler=handler.put_embed_files_handler
    )
  ]