from fastapi import HTTPException
from src.exceptions import ExceptionAbstract

class NotFoundError(ExceptionAbstract):
  def __init__(self, message):
    super().__init__(status_code=404, message=message)

  def throw(self):
    return HTTPException(status_code=self.status_code, detail=self.message)