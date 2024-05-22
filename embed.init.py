from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import EMBED_MODEL_PATH, BASE_KNOWLEDGE_DOCUMENT_PATH, BASE_KNOWLEDGE_DOCUMENT_NAME, TEXT_GENERATION_MODEL_PATH

# load the readable document
doc = PyPDFLoader(f"{BASE_KNOWLEDGE_DOCUMENT_PATH}/{BASE_KNOWLEDGE_DOCUMENT_NAME}").load()

# split the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)
splitted_doc = text_splitter.split_documents(doc)

# embed the splitted document using particular embedding model
# cuda out of memory using GTX 1650 4 Gb. If the PC has a good specs, delete {'device': 'cpu'} for faster processing
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_PATH, model_kwargs={'trust_remote_code': True, 'device': 'cpu'})
embedded_doc = FAISS.from_documents(splitted_doc, embedding_model)

# save embedded doc into local directory
embedded_doc.save_local(folder_path=f"{BASE_KNOWLEDGE_DOCUMENT_PATH}/embedding")