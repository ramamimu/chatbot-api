# python version : 3.8.10
# running on Ubuntu 20.04
# specs: memory 16Gb, GTX 1650 4Gb

import fastapi
# 0.111.0
print(fastapi.__version__)

import lorem_text
# 2.1
print(lorem_text.__version__)

import requests
# 2.31.0
print(requests.__version__)

import sse_starlette
# 2.1.0
print(sse_starlette.__version__)

import huggingface_hub
# 0.23.1
print(huggingface_hub.__version__)

import langchain_community
# 0.2.0
print(langchain_community.__version__)

import pypdf
# 4.2.0
print(pypdf.__version__)

import sentence_transformers
# 2.7.0
print(sentence_transformers.__version__)

import faiss
# faiss cpu 1.8.0
print(faiss.__version__)

import alembic
# 1.13.1
print(alembic.__version__)

import psycopg2
# 160000 
# I thought it is not a version
print(psycopg2.__libpq_version__)

import pytest
# 8.2.1
print(pytest.__version__)

import pytest_cov
# 5.0.0
print(pytest_cov.__version__)

import pytest_asyncio
# 0.23.7
print(pytest_asyncio.__version__)

# checking by pip3 show aiofiles
# aiofiles 23.2.1

import asyncpg
# 0.29.0
print(asyncpg.__version__)

import langchain_community
# 0.2.0
print(langchain_community.__version__)