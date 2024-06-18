from typing import Optional
from pydantic import BaseModel

class PostQuestionStreamGeneratorType(BaseModel):
  id: str
  question: str
  isBahasa: bool

class PostQuestionSimilaritySearchType(BaseModel):
  question: str