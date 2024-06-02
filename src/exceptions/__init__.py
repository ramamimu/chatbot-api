from abc import ABC, abstractmethod
from fastapi import HTTPException

class ExceptionAbstract(ABC):
  def __init__(self, status_code):
    self.status_code = status_code

  @abstractmethod
  def throw(self, message):
    '''
    implementation:
    
    return HTTPException(status_code=self.status_code, detail=message)
    '''
    pass
