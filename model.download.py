import os 

from huggingface_hub import snapshot_download, login
from dotenv import load_dotenv
from config import EMBED_MODEL_PATH, EMBED_MODEL_NAME

load_dotenv()
login(os.getenv("HUGGINGFACEHUB_API_TOKEN"))

models = {
  "indo_sentence": "firqaaa/indo-sentence-bert-base",
  "finetuning-e5-small": "ramamimu/finetuning-MiniLM-L12-v2",
  "multilingual-e5-small": "intfloat/multilingual-e5-small",
}

print(f"============ downloading {EMBED_MODEL_NAME}(============")
snapshot_download(repo_id=models[EMBED_MODEL_NAME],
                   local_dir=EMBED_MODEL_PATH)
