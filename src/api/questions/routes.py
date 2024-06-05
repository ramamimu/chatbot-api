from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType

def routes(handler) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
        method=Method.POST.value,
        path="/questions/stream-generator",
        handler=handler.post_question_stream_generator_handler
    ),
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions",
      handler=handler.post_question_stream_handler
    ),
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions/topic/{topic_name}",
      handler=handler.post_questions_by_topic_name_handler
    ),
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions/similarity-search",
      handler=handler.post_question_similarity_search_handler
    )
  ]