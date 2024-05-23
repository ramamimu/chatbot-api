from typing import List
from langchain_community.vectorstores import FAISS
import os

from config import BASE_KNOWLEDGE_DOCUMENT_PATH
from src.services.postgres.models.tables import Files

class VectorstoreService:
  def __init__(self, embedding_model, files_db_service) -> None:
    self._embedding_model = embedding_model
    self._vectorstore = FAISS.load_local(folder_path=f"{BASE_KNOWLEDGE_DOCUMENT_PATH}/embedding", embeddings=self._embedding_model, allow_dangerous_deserialization=True)
    self._files_db_service = files_db_service

  def load_all_local_embedding(self):
    files = self._files_db_service.get_all_file()
    for file in files:
      self.add_vectostore(file.path)
  
  def add_vectostore(self, path):
    embedding_path = f"{path}/embedding"
    if os.path.exists(embedding_path):
      local_vectorstore = FAISS.load_local(folder_path=embedding_path, embeddings=self._embedding_model, allow_dangerous_deserialization=True)
      self._vectorstore.merge_from(local_vectorstore)
    else:
      self._files_db_service.delete_file_by_id(path)
