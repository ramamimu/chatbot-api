import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from src.server.endpoint_factory import EndpointFactory

# services
from src.services.generator.lorem_generator_service import LoremGeneratorService

# endpoints
import src.api.questions as questions
import src.api.health_check as health_check

# NOTES
# regular method is for accessing self variable
# classmethod is able as alternative constructor
# staticmethod is for accessing class which have no relation on instance class

class Server:
  def __init__(self, port: int) -> None:
    self._app = FastAPI()
    self.port = port
  
  def configure_middleware(self):
    self._app.add_middleware(
      CORSMiddleware,
      allow_origins=['*'],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
    )
  
  def configure_endpoint(self):
    lorem_generator_service = LoremGeneratorService()

    endpoint_factory = EndpointFactory(self._app)
    endpoint_factory.routes_creator(questions.register(lorem_generator_service))
    endpoint_factory.routes_creator(health_check.register())

  def run(self):
    uvicorn.run(self._app, host="0.0.0.0", port=self.port)
