from fastapi import UploadFile
from pydantic import BaseModel

class DeleteFileKnowledgeType(BaseModel):
    id: int
    name: str
