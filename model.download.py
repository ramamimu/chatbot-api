import os 

from huggingface_hub import snapshot_download, login
from dotenv import load_dotenv

load_dotenv()
login(os.getenv("HUGGINGFACEHUB_API_TOKEN"))

prefix_dir = "./src/commons/models"

models = {
  "indo_sentence": {
    "repo_id": "firqaaa/indo-sentence-bert-base",
    "local_dir": f"{prefix_dir}/indo-sentence-bert-base"
  },
  "gpt2": {
    "repo_id": "openai-community/gpt2",
    "local_dir": f"{prefix_dir}/gpt2"
  },
  "komodo": {
    "repo_id": "Yellow-AI-NLP/komodo-7b-base",
    "local_dir": f"{prefix_dir}/komodo"
  },
  "mistral": {
    "repo_id": "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ",
    "local_dir": f"{prefix_dir}/mistral"
  },
  "llama2": {
    "repo_id": "meta-llama/Llama-2-7b-chat-hf",
    "local_dir": f"{prefix_dir}/llama2"
  },
  "sealion": {
    "repo_id": "aisingapore/sea-lion-7b-instruct",
    "local_dir": f"{prefix_dir}/sealion"
  }
}

snapshot_download(repo_id=models["indo_sentence"]["repo_id"],
                   local_dir=models["indo_sentence"]["local_dir"])
