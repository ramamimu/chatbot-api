from sse_starlette.sse import EventSourceResponse
from lorem_text import lorem
import asyncio
import random
from typing import List

class LoremGeneratorService:
  def __init__(self) -> None:
    pass
  
  async def generate_lorem(self):
    # solver: https://stackoverflow.com/questions/75740652/fastapi-streamingresponse-not-streaming-with-generator-function
    # docs: https://github.com/sysid/sse-starlette
    return EventSourceResponse(self.lorem_generator(), media_type='text/event-stream')

  @staticmethod
  async def lorem_generator():
    randomizer = random.randint(1, 5)
    lorem_text:str = lorem.paragraphs(randomizer)
    splitted_lorem:List[str] = lorem_text.split(' ')
    
    new_text = ""
    for i in splitted_lorem:
      new_text += f"{i} "
      yield f"{i} "
      await asyncio.sleep(0.1)