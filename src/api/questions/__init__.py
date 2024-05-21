from src.api.questions.handler import QuestionsHandler
from src.api.questions.routes import routes

def register(lorem_generator_service):
  questions_handler = QuestionsHandler(lorem_generator_service)
  return routes(questions_handler)