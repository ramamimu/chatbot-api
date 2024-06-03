from abc import ABC, abstractmethod
from fastapi import HTTPException

class ExceptionAbstract(ABC):
  def __init__(self, status_code:int, message:str):
    self.status_code = status_code
    self.message = message

  @abstractmethod
  def throw(self):
    '''
    implementation:
    
    return HTTPException(status_code=self.status_code, detail=self.message)
    '''
    pass
