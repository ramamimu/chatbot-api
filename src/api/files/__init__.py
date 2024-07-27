from src.api.files.handler import FilesHandler
from src.api.files.utils import FileUtils
from src.api.files.routes import routes

def register(file_storage_service, files_db_service, embedding_service, vectorstore_service, memorystore_service):
  file_utils = FileUtils()
  files_handler = FilesHandler(file_utils, file_storage_service, files_db_service, embedding_service, vectorstore_service, memorystore_service)
  return routes(files_handler)