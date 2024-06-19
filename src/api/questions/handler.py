from src.commons.types.questions_api_handler_type import PostQuestionStreamGeneratorType, PostQuestionSimilaritySearchType
from sse_starlette.sse import EventSourceResponse

class QuestionsHandler:
  def __init__(self, lorem_generator_service, chain_service, vectorstore_service, memorystore_service):
    self._lorem_generator_service = lorem_generator_service
    self._chain_service = chain_service
    self._vectorstore_service = vectorstore_service
    self._memorystore_service = memorystore_service
  
  async def post_question_stream_generator_handler(self, payload: PostQuestionStreamGeneratorType):
    # ignore the id and question
    return await self._lorem_generator_service.generate_lorem()
  
  async def post_question_stream_handler(self, payload: PostQuestionStreamGeneratorType):
    self._memorystore_service.add_user_message(payload.id, payload.question)

    return EventSourceResponse(self._chain_streamer(payload.question, payload.id), media_type='text/event-stream')

  async def _chain_streamer(self, question, id, is_output_html=True):
      memorystore = self._memorystore_service.get_memory(id)
      context = self._chain_service.get_context(question, memorystore)
      chain_gen = self._chain_service.get_chain(is_stream=True, is_output_html=is_output_html).astream(context)
      
      accumulated_text = ""
      async for chunk in chain_gen:
          accumulated_text += chunk
          yield chunk
      
      # After the streaming is complete, add the accumulated text to the memory store
      self._memorystore_service.add_ai_message(id, accumulated_text)

  async def post_question_no_stream_handler(self, payload: PostQuestionStreamGeneratorType):
    self._memorystore_service.add_user_message(payload.id, payload.question)
    memorystore = self._memorystore_service.get_memory(payload.id)
    context = self._chain_service.get_context(payload.question, memorystore)
    answer = self._chain_service.get_chain(is_stream=False, is_output_html=False).invoke(context)
    self._memorystore_service.add_ai_message(payload.id, answer)
    return answer

  async def post_question_similarity_search_handler(self, payload: PostQuestionSimilaritySearchType):
    return self._vectorstore_service.similarity_search(payload.question)