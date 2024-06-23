import os 

from huggingface_hub import snapshot_download, login
from dotenv import load_dotenv
from config import EMBED_MODEL_PATH, EMBED_MODEL_NAME

load_dotenv()
login(os.getenv("HUGGINGFACEHUB_API_TOKEN"))

print(f"============ downloading {EMBED_MODEL_NAME}(============")
snapshot_download(repo_id=EMBED_MODEL_NAME,
                   local_dir=EMBED_MODEL_PATH)
