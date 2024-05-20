import uvicorn
from lorem_text import lorem
from typing import List
import random
from config import PORT
import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

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
    self._app.get("/ping")(self.health_check)
    self._app.get("/generate_stream")(self.generate_stream)

  def run(self):
    uvicorn.run(self._app, host="0.0.0.0", port=self.port)

  def health_check():
    return "pong"

  async def generate_stream(self):
    # solver: https://stackoverflow.com/questions/75740652/fastapi-streamingresponse-not-streaming-with-generator-function
    # docs: https://github.com/sysid/sse-starlette
    return EventSourceResponse(self.lorem_generator(), media_type='text/event-stream')

  async def lorem_generator():
    randomizer = random.randint(1, 5)
    lorem_text:str = lorem.paragraphs(randomizer)
    splitted_lorem:List[str] = lorem_text.split(' ')
    
    new_text = ""
    for i in splitted_lorem:
      new_text += f"{i} "
      yield f"{i} "
      await asyncio.sleep(0.1)

