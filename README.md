# Chatbot API

## how to run manually

> if run manually, only supported on unix

- create virtual environment

  ```
  python3 -m venv venv

  source venv/bin/activate
  ```

- install packages

  Highly recommend to install package manually as put in `installer.txt`

  or

  ```
  pip3 install -r requirements.txt
  ```

- create `.env` such `example.env` file

- setup database

  setup the database as put in `.env` file. then create database name `chatbot`

  ```
  CREATE DATABASE chatbot
  ```

  or you can simply use docker compose of postgres in `compose/postgres.yaml`

- Apply the Alembic migrations

  ```
  make migrate-checkout r=head
  ```

- download embeeding model

  ```
  python3 model.download.py
  ```

- embed basic knowledge for vectorstore db

  ```
  python3 embed.init.py
  ```

- run the app

  for development

  ```
  python3 app.py
  ```

  for deployment testing

  ```
  fastapi run app.py
  ```

## how to run using docker

1. create .env such example.env file

2. run dockercompose command

```
docker compose build --no-cache
```

```
docker compose up -d
```

`-d` means running as daemon

exposing `port 5001` as default

> sometimes, the code was error. Keep build the image untill get succeed then `compose up`

## how to add preprocessing file

you need to configure of three things:

1. create folder name in following rule `documents/preprocessing-<your custom name>`

2. provide `.pdf` file in your directory as downloadable file later on

3. provide `.txt` file in your directory which contains `.pdf` file content as chatbot knowledge due to not all `.pdf` file is readable

the program will automatically recognize as preprocessing stuff and will be loaded when it get starts.

## documentation

Documentation able to see on `url/docs`. It is generated automatically by fastapi. It also provides API playground.

## useful link references

- stream communication: https://github.com/sysid/sse-starlette
