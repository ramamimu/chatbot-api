from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS

import os

from config import TEXT_GENERATION_MODEL, BASE_KNOWLEDGE_DOCUMENT_PATH

class ChainService:
  def __init__(self, files_db_service, vectorstore_service) -> None:
    self._files_db_service = files_db_service
    self._vectorstore_service = vectorstore_service

  def _init_prompt(self, is_output_html):
    '''
    Prompt engineer works here :)
    '''
    template = """
      SYSTEM: Anda adalah chatbot interaktif bernama Tanyabot. Anda bertugas untuk menjawab pertanyaan seputar akademik Teknik Informatika ITS.
      Ikuti instruksi ini untuk menjawab pertanyaan: jawablah pertanyaan dari context yang telah diberikan. Jika Anda tidak berhasil mendapatkan jawaban, katakan "saya tidak tahu".
      Ubah struktur kalimat menjadi HTML tapi hanya gunakan tag <ul> <ol> <li> <p> <br> <h2> <h3> <b> <strong>.      
      Context: {context}
      
      Question: {question}
    """ if is_output_html else """
      SYSTEM: Anda adalah chatbot interaktif bernama Tanyabot. Anda bertugas untuk menjawab pertanyaan seputar akademik Teknik Informatika ITS.
      Ikuti instruksi ini untuk menjawab pertanyaan: jawablah pertanyaan dari context yang telah diberikan. Jika Anda tidak berhasil mendapatkan jawaban, katakan "saya tidak tahu".
      Context: {context}

      Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt
  
  def _init_llm(self, is_stream: bool):
    return ChatOpenAI(model_name=TEXT_GENERATION_MODEL, temperature=0.3, streaming=is_stream)

  def get_chain(self, is_stream: bool, id: str, is_output_html = True):
    '''
    The chain will automatically update since vectorstore update even with no reinitialization
    '''
    chain = (
      {
        "context": self._vectorstore_service.get_retriever(), 
        "question": RunnablePassthrough()
      }
      | self._init_prompt(is_output_html)
      | self._init_llm(is_stream)
      | StrOutputParser()
    )
    return chain

