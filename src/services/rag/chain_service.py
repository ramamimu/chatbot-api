from typing import Type
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import TEXT_GENERATION_MODEL, BASE_KNOWLEDGE_DOCUMENT_PATH
from src.services.postgres.files_db_service import FilesDbService
from src.services.rag.vectorstore_service import VectorstoreService

class ChainService:
  def __init__(self, files_db_service, vectorstore_service) -> None:
    self._files_db_service: Type[FilesDbService] = files_db_service
    self._vectorstore_service: Type[VectorstoreService] = vectorstore_service

  def create_chain(self, retriever_func):
    return (
      {
        "context": retriever_func(),
        "question": RunnablePassthrough()
      }
      | self._init_prompt()
      | self._init_llm()
      | StrOutputParser()
    )

  def _init_prompt(self):
    '''
    Prompt engineer works here :)
    '''
    template = """SYSTEM: Anda adalah chatbot interaktif bernama Tanyabot. 
      Ikuti instruksi ini untuk menjawab pertanyaan: jawablah pertanyaan dari context yang telah diberikan. Jangan menjawab di luar konteks yang telah diberikan. Jika Anda mendapatkan jawaban di luar konteks yang telah diberikan atau tidak berhasil mendapatkan jawaban, katakan "saya tidak tahu".
      Context: {context}

      Question: {question}
      Ubah struktur kalimat menjadi HTML tapi hanya gunakan tag <ul> <ol> <li> <p> <br> <h2> <h3> <b> <strong>.    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt
  
  def _init_llm(self):
    return ChatOpenAI(model_name=TEXT_GENERATION_MODEL, temperature=0, streaming=True)

