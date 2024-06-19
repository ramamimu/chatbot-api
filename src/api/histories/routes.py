from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
      method=Method.GET.value,
      path="/history",
      handler=handler.get_history_handler
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/history/list",
      handler=handler.get_history_list_handler
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/history/{history_id}",
      handler=handler.get_history_by_id_handler
    ),
    HandlerRequestType(
      method=Method.DELETE.value,
      path="/history/{history_id}",
      handler=handler.delete_history_by_id_handler
    ),
      HandlerRequestType(
      method=Method.DELETE.value,
      path="/history",
      handler=handler.delete_history_handler
    ),
  ]