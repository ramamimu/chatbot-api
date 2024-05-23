from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from config import EMBED_MODEL_PATH

class EmbeddingService:
  def __init__(self) -> None:
    self._splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap = 200,
    )
    self._embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_PATH, model_kwargs={'trust_remote_code': True})
  
  def split_document(self, path: str) -> List[Document]:
    document = PyPDFLoader(path).load()
    splitted_document = self._splitter.split_documents(document)
    return splitted_document
  
  def split_text(self, text: str) -> List[str]:
    return self._splitter.split_text(text)
  
  def embed_document(self, splitted_document: Document):
    embedded_document = FAISS.from_documents(splitted_document, self._embedding_model)
    return embedded_document
  
  def save_local_embedded_document(self, embedded_document, path):
    embedded_document.save_local(folder_path=f"{path}/embedding")



  