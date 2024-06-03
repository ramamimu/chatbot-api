from typing import List, Type

from src.commons.types.files_db_type import FilesEntity
from src.commons.types.topics_api_handler_type import DetailTopicEntity
from src.services.postgres.models.tables import Files, Topics


def detail_topic_entity(topic: Topics, files: List[Type[Files]]) -> DetailTopicEntity:
  filesEntity = [ 
    FilesEntity(
        id=file.id,
        filename=file.file_name,
        name=file.custom_name,
        created=file.created,
        lastModified=file.last_modified
      )
     for file in files
    ]
    
  return DetailTopicEntity(
    topicId=topic.id,
    topicName=topic.name,
    files=filesEntity
  )