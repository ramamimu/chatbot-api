from typing import List
from src.commons.constant.method_http import Method
from src.commons.types.handler_request_type import HandlerRequestType


class EndpointFactory:
  def __init__(self, app) -> None:
    self._app = app
  
  def routes_creator(self, routes: List[HandlerRequestType]):
    for route in routes:
      self._create(route)

  def _create(self, endpoint: HandlerRequestType):
    if endpoint.method == Method.GET.value:
      return self._app.get(endpoint.path, status_code=self._status_code_handler(endpoint))(endpoint.handler)
    elif endpoint.method == Method.POST.value:
      return self._app.post(endpoint.path, status_code=self._status_code_handler(endpoint))(endpoint.handler)
    elif endpoint.method == Method.PUT.value:
      return self._app.put(endpoint.path, status_code=self._status_code_handler(endpoint))(endpoint.handler)
    elif endpoint.method == Method.DELETE.value:
      return self._app.delete(endpoint.path, status_code=self._status_code_handler(endpoint))(endpoint.handler)
    else:
      raise Exception(f"method {endpoint.method} not registered")

  @staticmethod
  def _status_code_handler(endpoint: HandlerRequestType):
    if endpoint.status_code is None:
      return 200
    
    return endpoint.status_code