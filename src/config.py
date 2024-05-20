import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")