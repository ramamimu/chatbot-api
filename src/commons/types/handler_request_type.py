from typing import Callable
from pydantic import BaseModel

class HandlerRequestType(BaseModel):
  method: str
  path: str
  handler: Callable