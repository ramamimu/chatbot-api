from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
      method=Method.POST.value,
      path="/topics",
      handler=handler.post_topic_handler,
      status_code=201
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/topics",
      handler=handler.get_topics_handler
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/topics/{topic_id}",
      handler=handler.get_topic_by_id_handler
    ),
    HandlerRequestType(
      method=Method.DELETE.value,
      path="/topics/{topic_id}",
      handler=handler.delete_topic_by_id_handler
    ),
    HandlerRequestType(
      method=Method.PUT.value,
      path="/topics/{topic_id}",
      handler=handler.put_topic_by_id_handler
    )
  ]