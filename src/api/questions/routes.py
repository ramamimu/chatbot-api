from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType

def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
        method=Method.POST.value,
        path="/questions/stream-generator",
        handler=handler.post_question_stream_generator_handler
    )
  ]