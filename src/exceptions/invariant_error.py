from fastapi import HTTPException
from src.exceptions import ExceptionAbstract

class InvariantError(ExceptionAbstract):
  '''
  Invariant error is caused of client mistake such as wrong syntax, file size too big, etc
  '''
  def __init__(self, message):
    super().__init__(status_code=400, message=message)
  
  def throw(self):
    return HTTPException(status_code=self.status_code, detail=self.message)