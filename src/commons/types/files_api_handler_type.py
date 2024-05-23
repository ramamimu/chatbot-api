from fastapi import UploadFile
from pydantic import BaseModel

class PutEmbedFilesType(BaseModel):
    name: str
    file: UploadFile