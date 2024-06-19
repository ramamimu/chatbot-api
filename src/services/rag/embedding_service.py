from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from config import EMBED_MODEL_PATH
import os

class EmbeddingService:
  def __init__(self, embedding_model, files_db_service) -> None:
    self._splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap = 200,
    )
    self._embedding_model = embedding_model
    self._files_db_service = files_db_service
  
  def split_document(self, path: str) -> List[Document]:
    document = PyPDFLoader(path).load()
    splitted_document = self._splitter.split_documents(document)
    return splitted_document
  
  def split_text(self, text: str) -> List[str]:
    return self._splitter.split_text(text)
  
  def embed_document(self, splitted_document: Document):
    embedded_document = FAISS.from_documents(splitted_document, self._embedding_model)
    return embedded_document

  def embed_text(self, splitted_text: List[str], metadatas):
    embedded_text = FAISS.from_texts(splitted_text, embedding=self._embedding_model, metadatas=metadatas)
    return embedded_text
  
  def save_embed_to_local(self, embedded_document, path):
    embedded_document.save_local(folder_path=f"{path}/embedding")

  def load_preprocessing_file(self):
    """
    1. get all files
    2. get file with prefix 'preprocessing-'
    3. check and get which file have not embedded
    4. embed those files
    5. add the remain file to vectorstore
    """
    files = self._files_db_service.get_all_file()
    file_db_dirs = [file.path for file in files]
    file_dirs = os.listdir("documents")
    file_preprocessing_dirs = [f"{file_dir}" for file_dir in file_dirs if "preprocessing-" in file_dir]
    for dir_name in file_preprocessing_dirs:
      dir_path = f"documents/{dir_name}"
      if dir_path not in file_db_dirs:

        # get txt file
        try:
          txt_file_path = [file for file in os.listdir(dir_path) if file.endswith('.txt')][0]
          pdf_file_path = [file for file in os.listdir(dir_path) if file.endswith('.pdf')][0]
        except:
          raise ValueError(f"{dir_name} don't have TXT or PDF file")

        txt_full_path = f"{dir_path}/{txt_file_path}"
        pdf_full_path = f"{dir_path}/{pdf_file_path}"
        # read text
        with open(txt_full_path, 'r') as file:
          content = file.read()
          # split text
          splitted_text = self.split_text(content)
          # set metadatas for every splitted text
          metadatas = []
          for text in splitted_text:
            metadatas.append({'source': pdf_full_path})
          # embed this file
          embedded_text = self.embed_text(splitted_text, metadatas)
          # save to local
          self.save_embed_to_local(embedded_text, dir_path)
          # write to db
          self._files_db_service.add_file(dir_name, pdf_file_path, dir_path)
          print("success to preprocessing embed ", dir_path)


  