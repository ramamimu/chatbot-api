from typing import Type
from src.commons.types.questions_api_handler_type import PostQuestionStreamGeneratorType, PostQuestionSimilaritySearchType
from sse_starlette.sse import EventSourceResponse

from src.services.rag.chain_service import ChainService
from src.services.rag.vectorstore_topic_service import VectorstoreTopicService

class QuestionsHandler:
  def __init__(self, lorem_generator_service, chain_service, vectorstore_service, vectorstore_topic_service):
    self._lorem_generator_service = lorem_generator_service
    self._chain_service: Type[ChainService] = chain_service
    self._vectorstore_service = vectorstore_service
    self._vectorstore_topic_service: Type[VectorstoreTopicService] = vectorstore_topic_service
  
  async def post_question_stream_generator_handler(self, payload: PostQuestionStreamGeneratorType):
    # ignore the id and question
    return await self._lorem_generator_service.generate_lorem()
  
  async def post_question_stream_handler(self, payload: PostQuestionStreamGeneratorType):
    question = f"{payload.question}. Jawab menggunakan Bahasa Indonesia!" if payload.isBahasa else f"{payload.question}. please answer in English!" 
    chain = self._chain_service.get_chain()
    return EventSourceResponse(self._chain_streamer(question, payload.id, chain), media_type='text/event-stream')

  async def _chain_streamer(self, question, id, chain):
    async for chunk in chain.astream(question):
        yield chunk

  async def post_question_similarity_search_handler(self, payload: PostQuestionSimilaritySearchType):
    return self._vectorstore_service.similarity_search(payload.question)
  
  async def post_questions_by_topic_name_handler(self, topic_name, payload: PostQuestionStreamGeneratorType):
    question = f"{payload.question}. Jawab menggunakan Bahasa Indonesia!" if payload.isBahasa else f"{payload.question}. please answer in English!" 
    retriever = self._vectorstore_topic_service.get_retriever_topic(topic_name)
    chain = self._chain_service.get_chain(retriever)
    return EventSourceResponse(self._chain_streamer(question, payload.id, chain))