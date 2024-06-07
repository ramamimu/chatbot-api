from typing import List, Type
from langchain_community.vectorstores import FAISS
import os

from config import BASE_KNOWLEDGE_DOCUMENT_PATH
from src.services.postgres.files_db_service import FilesDbService

class VectorstoreService:
  def __init__(self, embedding_model, files_db_service) -> None:
    self._embedding_model = embedding_model
    self._vectorstore = self.init_vectorstore()
    self._files_db_service: Type[FilesDbService] = files_db_service
  
  def init_vectorstore(self):
    return FAISS.load_local(folder_path=f"{BASE_KNOWLEDGE_DOCUMENT_PATH}/embedding", embeddings=self._embedding_model, allow_dangerous_deserialization=True)

  def get_retriever(self, vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 3})
  
  def get_vectorstore_by_files_id(self, files_id: List[str]):
    vectorstore = self.init_vectorstore()

    # prevent error when files_id is empty
    if len(files_id) <= 0:
      return vectorstore

    files = self._files_db_service.get_files_by_id(files_id)
    
    for file in files:
      embedding_path = f"{file.path}/embedding"
      if os.path.exists(embedding_path):
        temp_vectorstore = FAISS.load_local(folder_path=embedding_path, embeddings=self._embedding_model, allow_dangerous_deserialization=True)
        vectorstore.merge_from(temp_vectorstore)
      else:
        self._files_db_service.delete_file_by_id(embedding_path)
    
    return vectorstore

