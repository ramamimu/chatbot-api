from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os

from config import TEXT_GENERATION_MODEL, BASE_KNOWLEDGE_DOCUMENT_PATH

class ChainService:
  def __init__(self, files_db_service, vectorstore_service) -> None:
    self._files_db_service = files_db_service
    self._vectorstore_service = vectorstore_service
    self._chain = self._init_chain()

  def _init_chain(self):
    return (
      {
        "context": self._vectorstore_service.get_retriever(), 
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
    template = """SYSTEM: Anda adalah chatbot interaktif bernama Tanyabot, jawablah pertanyaan dari konteks yang diberikan. Jika Anda tidak mengetahui jawabannya, katakan "saya tidak tahu".
      Ubah struktur kalimat menjadi HTML tapi hanya gunakan tag <ul> <ol> <li> <p> <br> <h2> <h3> <b> <strong>.
      CONTEXT: {context}

      Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt
  
  def _init_llm(self):
    return ChatOpenAI(model_name=TEXT_GENERATION_MODEL, temperature=0, streaming=True)

  def get_chain(self):
    '''
    The chain will automatically update since vectorstore update even with no reinitialization
    '''
    return self._chain

