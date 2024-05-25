from src.commons.types.questions_api_handler_type import PostQuestionStreamGeneratorType
from sse_starlette.sse import EventSourceResponse

class QuestionsHandler:
  def __init__(self, lorem_generator_service, chain_service):
    self._lorem_generator_service = lorem_generator_service
    self._chain_service = chain_service
  
  async def post_question_stream_generator_handler(self, payload: PostQuestionStreamGeneratorType):
    # ignore the id and question
    return await self._lorem_generator_service.generate_lorem()
  
  async def post_question_stream_handler(self, payload: PostQuestionStreamGeneratorType):
    question = f"{payload.question}. Jawab menggunakan Bahasa Indonesia!" if payload.isBahasa else f"{payload.question}. please answer in English!" 
    return EventSourceResponse(self._chain_streamer(question, payload.id), media_type='text/event-stream')

  async def _chain_streamer(self, question, id):
    async for chunk in self._chain_service.get_chain().astream(question):
        yield chunk

