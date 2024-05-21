from pydantic import BaseModel

class PostQuestionStreamGeneratorType(BaseModel):
  id: str
  question: str