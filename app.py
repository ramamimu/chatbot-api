from lorem_text import lorem
from typing import List
import random
import uvicorn
from config import PORT

import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def health_check():
  return "pong"

async def lorem_generator():
  randomizer = random.randint(1, 5)
  lorem_text:str = lorem.paragraphs(randomizer)
  splitted_lorem:List[str] = lorem_text.split(' ')
  
  new_text = ""
  for i in splitted_lorem:
    new_text += f"{i} "
    # print(new_text)
    # yield f'{new_text}'
    yield f"{i} "
    await asyncio.sleep(0.1)

@app.get("/generate_stream")
async def generate_stream():
  # solver: https://stackoverflow.com/questions/75740652/fastapi-streamingresponse-not-streaming-with-generator-function
  # docs: https://github.com/sysid/sse-starlette
  return EventSourceResponse(lorem_generator(), media_type='text/event-stream')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))