from src.api.topics.routes import routes
from src.api.topics.handler import TopicsHandler

def register(files_db_service, topics_db_service, topic_files_db_service, vectorstore_topic_service):
  topics_handler = TopicsHandler(files_db_service, topics_db_service, topic_files_db_service, vectorstore_topic_service)
  return routes(topics_handler)