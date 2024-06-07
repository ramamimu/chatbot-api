import json
from typing import List, Type

from src.commons.types.files_api_handler_type import Topic
from src.commons.types.files_db_type import FilesEntity
from src.commons.types.topics_api_handler_type import DetailTopicEntity
from src.exceptions.invariant_error import InvariantError
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

def topics_form_payload(topics: str):
  try:
    topics_list = json.loads(topics)
    topic_objects = [Topic(id=int(topic['id']), name=topic['name']) for topic in topics_list]
    return topic_objects
  except Exception as e:
    print(e)
    raise InvariantError('topics payload is not valid')