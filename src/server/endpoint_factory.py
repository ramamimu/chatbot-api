from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


class EndpointFactory:
  def __init__(self, app) -> None:
    self._app = app
  
  def routes_creator(self, routes: List[HandlerRequestType]):
    for route in routes:
      self._create(route)

  def _create(self, handler_endpoint: HandlerRequestType):
    if handler_endpoint.method == Method.GET.value:
      return self._app.get(handler_endpoint.path)(handler_endpoint.handler)
    elif handler_endpoint.method == Method.POST.value:
      return self._app.post(handler_endpoint.path)(handler_endpoint.handler)
    elif handler_endpoint.method == Method.PUT.value:
      return self._app.put(handler_endpoint.path)(handler_endpoint.handler)
    elif handler_endpoint.method == Method.DELETE.value:
      return self._app.delete(handler_endpoint.path)(handler_endpoint.handler)
    else:
      raise Exception(f"method {handler_endpoint.method} not registered")

  