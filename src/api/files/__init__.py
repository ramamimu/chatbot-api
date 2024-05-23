from src.api.files.handler import FilesHandler
from src.api.files.routes import routes

def register(file_storage_service, files_db_service):
  files_handler = FilesHandler(file_storage_service, files_db_service)
  return routes(files_handler)