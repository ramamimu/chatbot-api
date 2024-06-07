from typing import List, Optional, Type
from fastapi import File, UploadFile, Form
from fastapi.responses import FileResponse

from src.commons.entities.files_db_entity import files_db_entity
from src.commons.entities.topics_entity import topics_form_payload
from src.commons.types.files_api_handler_type import DeleteFileKnowledgeType, Topic
from src.services.postgres.files_db_service import FilesDbService
from src.services.postgres.models.tables import Files, Topics
from src.services.postgres.topic_files_db_service import TopicFilesDbService
from src.services.postgres.topics_db_service import TopicsDbService
from src.services.rag.embedding_service import EmbeddingService
from src.services.rag.vectorstore_service import VectorstoreService
from src.services.rag.vectorstore_topic_service import VectorstoreTopicService
from src.services.storage.files_storage_service import FileStorageService

class FilesHandler:
  def __init__(self, file_storage_service, files_db_service, embedding_service, vectorstore_service, topics_db_service, topic_files_db_service, vectorstore_topic_service):
    self._file_storage_service: Type[FileStorageService] = file_storage_service
    self._files_db_service: Type[FilesDbService] = files_db_service
    self._embedding_service: Type[EmbeddingService] = embedding_service
    self._vectorstore_service: Type[VectorstoreService] = vectorstore_service
    self._topics_db_service: Type[TopicsDbService] = topics_db_service
    self._topic_files_db_service: Type[TopicFilesDbService] = topic_files_db_service
    self._vectorstore_topic_service: Type[VectorstoreTopicService] = vectorstore_topic_service

  async def put_embed_files_handler(self, name: str = Form(...), file: UploadFile  = File(...)):
    '''
    ## Posting new file as a new knowledge

    - verify existance topic ids 

    - create dir src/commons/<title> and return the path
    
    - save file in src/commons/<title>/<title.pdf>
    
    - write name and path in database
    
    - split document
    
    - embed document
    
    - save embedded document in local
    
    - update vectorstore topics based on the file
    '''
    full_path:str = await self._file_storage_service.save_file_to_folder(name, file)
    self._files_db_service.add_file(name, file.filename, full_path)
    splitted_document = self._embedding_service.split_document(f"{full_path}/{file.filename}")
    embedded_document = self._embedding_service.embed_document(splitted_document)
    self._embedding_service.save_embedded_document_to_local(embedded_document, full_path)
    return {"status":"success"}
  
  async def delete_file_handler(self, payload: DeleteFileKnowledgeType):
    '''
    for next iteration, `DELETE /files/knowledge` will replaced by `DELETE /files` with similar payload
    return type of `chunks` will deleted in the next iteration, so it just return `{"status":"success"}`

    - check is id and name available and return detail file

    - get all topics which are have this type of knowledge

    - delete the chunks in particular topic

    - repeat the method untill all of this included file knowledge has been deleted at all topics

    - repeat the method untill all of this included file knowledge has been deleted at all topics

    - delete file in directory

    - delete knowledge in all vectorstore
    '''
    
    file = self._files_db_service.verify_file_by_id_name(payload.id, payload.name)
    topics: List[Topics] = self._topic_files_db_service.get_topics_by_file_id(payload.id)
    for topic in topics:
      chunks: List[str] = self._vectorstore_topic_service.get_chunks_by_filename(file.file_name, topic.name)
      self._vectorstore_topic_service.delete_document_by_chunks(chunks, topic.name)

    self._files_db_service.delete_file_by_id(file.id)
    self._file_storage_service.delete_directory(file.path)

    return {
      "status": "success",
      "chunks": []
    }
    
  async def get_files_handler(self):
    files = self._files_db_service.get_all_files()
    return {
      "status": "success",
      "files": files_db_entity(files)
    }

  async def get_files_download_by_id_handler(self, file_id):
    '''
    1. verify id in db return file if available
    2. verify path existence in directory
    '''
    
    file = self._files_db_service.verify_file_by_id(file_id)
    self._file_storage_service.verify_path(f"{file.path}/{file.file_name}")
    return FileResponse(f"{file.path}/{file.file_name}", media_type='application/octet-stream', filename=file.file_name)
    
    