from pydantic import BaseModel
from datetime import datetime

class FilesEntity(BaseModel):
    id: int
    name: str
    filename: str
    created: datetime
    lastModified: datetime