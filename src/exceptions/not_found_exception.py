from fastapi import HTTPException
from src.exceptions import ExceptionAbstract

class NotFoundException(ExceptionAbstract):
  def __init__(self):
    super().__init__(status_code=404)

  def throw(self, message):
    return HTTPException(status_code=self.status_code, detail=message)