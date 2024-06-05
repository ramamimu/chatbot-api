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

  def get_retriever(self, vectorstore = None):
    retriever = None
    if vectorstore is None:
      retriever = self._vectorstore.as_retriever(search_kwargs={"k": 3})
    else:
      retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever
  
  def get_vectorstore(self):
    if self._vectorstore is None:
        raise ValueError("Vectorstore is None, expected a valid vectorstore instance.")
    return self._vectorstore
  
  def load_all_local_embedding(self):
    files = self._files_db_service.get_all_file()
    for file in files:
      print(f"{file.path} registered as knowledge")
      self.add_vectostore(file.path)
  
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

  def add_vectostore(self, path):
    embedding_path = f"{path}/embedding"
    if os.path.exists(embedding_path):
      local_vectorstore = FAISS.load_local(folder_path=embedding_path, embeddings=self._embedding_model, allow_dangerous_deserialization=True)
      self._vectorstore.merge_from(local_vectorstore)
    else:
      self._files_db_service.delete_file_by_id(path)
  
  def similarity_search(self, question):
    ss = self._vectorstore.similarity_search(question, k=3)
    return ss
  
  def get_chunks_by_filename(self, filename: str):
    vector_dict = self._vectorstore.docstore._dict
    chunks_id = []

    for id in vector_dict.keys():
      # get the last value of source which the filename
      doc_name = vector_dict[id].metadata["source"].split('/')[-1]
      if filename == doc_name:
        chunks_id.append(id)
    
    return chunks_id

  def delete_document_by_chunks(self, chunks):
    self._vectorstore.delete(chunks)