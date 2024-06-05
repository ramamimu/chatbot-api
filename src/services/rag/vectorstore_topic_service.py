from typing import List, Type

from src.exceptions.invariant_error import InvariantError
from src.services.postgres.models.tables import Files, Topics
from src.services.postgres.topic_files_db_service import TopicFilesDbService
from src.services.postgres.topics_db_service import TopicsDbService
from src.services.rag.vectorstore_service import VectorstoreService


class VectorstoreTopicService:
  def __init__(self, topics_db_service, topic_files_db_service, vectorstore_service) -> None:
    self._topic_store = {}
    self._topics_db_service: Type[TopicsDbService] = topics_db_service
    self._topic_files_db_service: Type[TopicFilesDbService] = topic_files_db_service
    self._vectorstore_service: Type[VectorstoreService] = vectorstore_service

  def load_topic_store(self):
    '''
    1. get all topics

    2. get all file id

    3. create new topic using files id
    '''
    topics: List[Type[Topics]] = self._topics_db_service.get_topics()
    for topic in topics:
      files: List[Type[Files]] = self._topic_files_db_service.get_files_by_topic(topic.id)
      self.create_new_topic(topic.name, [file.id for file in files])
      print(f"topic {topic.name} created to the store")

  def create_new_topic(self, topic_name: str, files_id: List[str]):
    vectorstore = self._vectorstore_service.get_vectorstore_by_files_id(files_id)
    self._topic_store[topic_name] = vectorstore
    
  def set_topic(self, topic_name, files_id):
    if topic_name in self._topic_store.keys():
      vectorstore = self.create_new_topic(topic_name, files_id)
      self._topic_store[topic_name].merge_from(vectorstore)
    else:
      self.create_new_topic(topic_name, files_id)

  def get_retriever_topic(self, topic_name):
    if topic_name in self._topic_store.keys():
      return self._vectorstore_service.get_retriever(self._topic_store[topic_name])
    else:
      raise InvariantError("topic not available").throw()
  
  def delete_topic(self, topic_name: str):
    if topic_name in self._topic_store.keys():
      self._topic_store.pop(topic_name)
    else:
      raise InvariantError("topic not available").throw()

  def get_all_topics_name(self):
    return list(self._topic_store.keys())
