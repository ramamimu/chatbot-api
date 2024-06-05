from typing import List, Type
from src.commons.entities.topics_entity import detail_topic_entity
from src.commons.types.topics_api_handler_type import PostTopicType
from src.services.postgres.files_db_service import FilesDbService
from src.services.postgres.models.tables import Files, Topics
from src.services.postgres.topic_files_db_service import TopicFilesDbService
from src.services.postgres.topics_db_service import TopicsDbService
from src.services.rag.vectorstore_topic_service import VectorstoreTopicService


class TopicsHandler():
  def __init__(self, files_db_service, topics_db_service, topic_files_db_service, vectorstore_topic_service) -> None:
    self._topics_db_service: Type[TopicsDbService] = topics_db_service
    self._files_db_service: Type[FilesDbService] = files_db_service
    self._topic_files_db_service: Type[TopicFilesDbService] = topic_files_db_service
    self._vectorstore_topic_service: Type[VectorstoreTopicService] = vectorstore_topic_service

  async def post_topic_handler(self, payload: PostTopicType):
    '''
    create new topic

    1. verify availability topic name

    2. input topic to topics table, return created topics detail

    3. verify all file name return files in detail

    4. input files of topic to files_topic table

    5. create new vectorstore topic
    '''
    self._topics_db_service.verify_availability_topic_name(payload.topicName)
    topic: Type[Topics] = self._topics_db_service.add_topic(payload.topicName)
    files = await self._files_db_service.verify_all_file_names_exist(payload.nameFiles) 
    self._vectorstore_topic_service.create_new_topic(payload.topicName, [ file.id for file in files ])
    # have no idea why add files topic method make the process deadlock when put after verify file names exist
    self._topic_files_db_service.add_files_topic(topic, files)
    return {"message": "success create topic"}

  async def get_topic_by_id_handler(self, topic_id):
    '''
    get detail topic

    1. verify topic is available
    
    2. get topic id and name
    
    3. get topic files
    '''
    self._topics_db_service.verify_existance_topic_by_id(topic_id)
    topic: Type[Topics] = self._topics_db_service.get_topic_by_id(topic_id)
    files: List[Type[Files]] = self._topic_files_db_service.get_files_by_topic(topic_id)
    return {
      "status": "success",
      "detailTopic": detail_topic_entity(topic, files)
    }

  async def get_topics_handler(self):
    '''
    get all topics
    '''
    topics: Type[Topics] = self._topics_db_service.get_topics()
    return {
      "status": "success",
      "topics": topics
    }

  async def delete_topic_by_id_handler(self, topic_id):
    '''
    1. verify existance topic

    2. delete topic in topic files table for avoiding foreign key deleted error

    3. delete topic in topic table

    4. delete topic in chain store
    '''
    topic: Type[Topics] = self._topics_db_service.verify_existance_topic_by_id(topic_id)
    self._topic_files_db_service.delete_topic_files_by_topic_id(topic_id)
    self._topics_db_service.delete_topic_by_id(topic_id)
    self._vectorstore_topic_service.delete_topic(topic.name)
    return {"message": "success delete topic"}

  async def put_topic_by_id_handler(self, topic_id, payload: PostTopicType):
    '''
    edit topic by id

    1. verify existance topic by id

    2. delete vectorstore topic

    3. update topic with current value

    4. delete files topic by topic id

    5. verify all filenames exist

    6. add new files topic

    7. create new topic

    '''
    topic: Type[Topics] = self._topics_db_service.verify_existance_topic_by_id(topic_id)
    self._vectorstore_topic_service.delete_topic(topic.name)
    topic: Type[Topics] = self._topics_db_service.update_topic_by_id(topic_id, payload.topicName)
    self._topic_files_db_service.delete_topic_files_by_topic_id(topic_id)
    files = await self._files_db_service.verify_all_file_names_exist(payload.nameFiles) 
    self._vectorstore_topic_service.create_new_topic(topic.name, [file.id for file in files])
    self._topic_files_db_service.add_files_topic(Topics(id=topic_id, name=payload.topicName), files, is_edit=True)

    return {"message": f"success edit {payload.topicName} topic"}