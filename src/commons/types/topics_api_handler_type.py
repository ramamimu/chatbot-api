from pydantic import BaseModel
from typing import List, Type

from src.commons.types.files_db_type import FilesEntity
from src.services.postgres.models.tables import Files

class PostTopicType(BaseModel):
  topicName: str
  nameFiles: List[str]

class DetailTopicEntity(BaseModel):
  topicId: int
  topicName: str
  files: List[FilesEntity]