from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType

def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions",
      handler=handler.post_question_stream_handler
    ),
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions/no-stream",
      handler=handler.post_question_no_stream_handler
    ),
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions/similarity-search",
      handler=handler.post_question_similarity_search_handler
    )
  ]