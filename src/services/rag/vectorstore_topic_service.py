from typing import List, Type

from src.exceptions.invariant_error import InvariantError
from src.services.postgres.models.tables import Files, Topics
from src.services.postgres.topic_files_db_service import TopicFilesDbService
from src.services.postgres.topics_db_service import TopicsDbService
from src.services.rag.vectorstore_service import VectorstoreService


class VectorstoreTopicService:
  def __init__(self, topics_db_service, topic_files_db_service, vectorstore_service) -> None:
    self._vectorstore_topic = {}
    self._topics_db_service: Type[TopicsDbService] = topics_db_service
    self._topic_files_db_service: Type[TopicFilesDbService] = topic_files_db_service
    self._vectorstore_service: Type[VectorstoreService] = vectorstore_service

  def load_topic_store(self):
    '''
    1. get all topics

    2. get all file id

    3. create root topic as base knowledge

    4. create new topic using files id
    '''
    
    topics: List[Type[Topics]] = self._topics_db_service.get_topics()
    for topic in topics:
      files: List[Type[Files]] = self._topic_files_db_service.get_files_by_topic(topic.id)
      self.create_new_topic(topic.name, [file.id for file in files])
      print(f"topic {topic.name} created to the store")
    
    # create root topic
    self.create_new_topic('root', [])

  def create_new_topic(self, topic_name: str, files_id: List[str]):
    vectorstore = self._vectorstore_service.get_vectorstore_by_files_id(files_id)
    self._vectorstore_topic[topic_name] = vectorstore

  def get_retriever_topic(self, topic_name):
    if topic_name in self._vectorstore_topic.keys():
      return self._vectorstore_service.get_retriever(self._vectorstore_topic[topic_name])
    else:
      raise InvariantError("topic not available").throw()
  
  def delete_topic(self, topic_name: str):
    if topic_name in self._vectorstore_topic.keys():
      self._vectorstore_topic.pop(topic_name)
    else:
      raise InvariantError("topic not available").throw()

  def get_all_topics_name(self):
    return list(self._vectorstore_topic.keys())
  
  def add_vectorstore_to_topic(self, topic_name, file_ids: List[str]):
    vectorstore_new_files = self._vectorstore_service.get_vectorstore_by_files_id(file_ids)
    self._vectorstore_topic[topic_name].merge_from(vectorstore_new_files)

  def get_chunks_by_filename(self, filename: str, topic_name):
    vector_dict = self._vectorstore_topic[topic_name].docstore._dict
    chunks_id = []

    for id in vector_dict.keys():
      # get the last value of source which the filename
      doc_name = vector_dict[id].metadata["source"].split('/')[-1]
      if filename == doc_name:
        chunks_id.append(id)
    
    return chunks_id
  
  def delete_document_by_chunks(self, chunks, topic_name):
    self._vectorstore_topic[topic_name].delete(chunks)

  def similarity_search(self, question, topic_name='root'):
    ss = self._vectorstore_topic[topic_name].similarity_search(question, k=3)
    return ss
