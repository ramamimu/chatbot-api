from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage

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
    system_msg = (
      "Anda adalah chatbot interaktif bernama Tanyabot.\n"
      "Ikuti instruksi ini untuk menjawab pertanyaan/question: jawablah pertanyaan/question dari context yang telah diberikan. Berikan jawaban yang relevan dan ika Anda tidak berhasil mendapatkan jawabannya, katakan 'saya tidak tahu'.\n"
    )
    
    system_msg = (system_msg + "Ubah struktur kalimat menjadi HTML tapi hanya gunakan tag <ul> <ol> <li> <p> <br> <h2> <h3> <b> <strong>.\n") if is_output_html else ""
    prompt = ChatPromptTemplate.from_messages(
      [
        (
          "system",
          system_msg
        ),
        MessagesPlaceholder(variable_name="context"),
        MessagesPlaceholder(variable_name="messages")
      ]
    )
    return prompt
  
  def _init_llm(self, is_stream: bool):
    return ChatOpenAI(model_name=TEXT_GENERATION_MODEL, temperature=0.5, streaming=is_stream)

  def get_chain(self, is_stream: bool, is_output_html = True):
    '''
    The chain will automatically update since vectorstore update even with no reinitialization
    '''
    chain = (
      self._init_prompt(is_output_html)
      | self._init_llm(is_stream)
      | StrOutputParser()
    )
    return chain

  @staticmethod
  def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

  def get_context(self, question, memorystore):
    context = self._vectorstore_service.similarity_search(question)
    return {
      "context": [HumanMessage(content=self._format_docs(context))],
      "messages": memorystore.messages
    }