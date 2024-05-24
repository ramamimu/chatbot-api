from typing import Optional
from pydantic import BaseModel

class PostQuestionStreamGeneratorType(BaseModel):
  id: Optional[str] = None
  question: str
  is_bahasa: bool