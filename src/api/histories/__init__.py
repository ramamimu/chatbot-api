from src.api.histories.handler import HistoriesHandler
from src.api.histories.routes import routes

def register(memorystore_service):
  histories_handler = HistoriesHandler(memorystore_service)
  return routes(histories_handler)