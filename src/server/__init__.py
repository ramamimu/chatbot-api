import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import DB_URI_TEST, EMBED_MODEL_PATH
from src.server.endpoint_factory import EndpointFactory

# services
from src.services.generator.lorem_generator_service import LoremGeneratorService
from src.services.storage.files_storage_service import FileStorageService
from src.services.postgres.files_db_service import FilesDbService
from src.services.postgres import PostgresDb
from src.services.rag.embedding_service import EmbeddingService
from src.services.rag.vectorstore_service import VectorstoreService
from src.services.rag.chain_service import ChainService
from src.services.rag.memorystore_service import MemorystoreService

# endpoints
import src.api.questions as questions_endpoint
import src.api.health_check as health_check_endpoint
import src.api.files as files_endpoint
import src.api.histories as histories_endpoint

# NOTES
# regular method is for accessing self variable
# classmethod is able as alternative constructor
# staticmethod is for accessing class which have no relation on instance class

class Server:
  def __init__(self, port: int, is_test_mode: bool) -> None:
    self._app = FastAPI()
    self.port = port
    self._is_test_mode = is_test_mode
  
  def configure_middleware(self):
    self._app.add_middleware(
      CORSMiddleware,
      allow_origins=['*'],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
    )
  
  def configure_endpoint(self):
    db = PostgresDb()
    embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_PATH, model_kwargs={'trust_remote_code': True})

    # service initiation
    lorem_generator_service = LoremGeneratorService()
    file_storage_service = FileStorageService()
    files_db_service = FilesDbService(db)
    embedding_service = EmbeddingService(embedding_model, files_db_service)
    vectorstore_service = VectorstoreService(embedding_model, files_db_service)
    chain_service = ChainService(files_db_service, vectorstore_service)
    memorystore_service = MemorystoreService()

    # service builder
    embedding_service.load_preprocessing_file()
    vectorstore_service.load_all_local_embedding()

    # routes initiation
    endpoint_factory = EndpointFactory(self._app)
    endpoint_factory.routes_creator(health_check_endpoint.register())
    endpoint_factory.routes_creator(questions_endpoint.register(lorem_generator_service, chain_service, vectorstore_service, memorystore_service))
    endpoint_factory.routes_creator(files_endpoint.register(file_storage_service, files_db_service, embedding_service, vectorstore_service, memorystore_service))
    endpoint_factory.routes_creator(histories_endpoint.register(memorystore_service))

  def run(self):
    uvicorn.run(self._app, host="0.0.0.0", port=self.port)
