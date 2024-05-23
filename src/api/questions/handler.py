from src.commons.types.questions_api_handler_type import PostQuestionStreamGeneratorType

class QuestionsHandler:
  def __init__(self, lorem_generator_service):
    self._lorem_generator_service = lorem_generator_service
  
  async def post_question_stream_generator_handler(self, payload: PostQuestionStreamGeneratorType):
    # ignore the payload and question
    return await self._lorem_generator_service.generate_lorem()
    

