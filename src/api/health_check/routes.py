from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
      method=Method.GET.value,
      path="/ping",
      handler=handler.get_ping
    )
  ]