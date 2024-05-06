# Chatbot API

## how to run manually

- create virtual environment

```
python3 -m venv venv

source venv/bin/activate
```

- Install packages

Highly recommended to install package manually as put in `installer.txt`

or

```
pip3 install -r requirements.txt
```

- create `.env` such `example.env` file

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

```
docker compose build --no-cache
```

```
docker compose up -d
```

`-d` means running as daemon

exposing `port 8000` as default

## documentation

Documentation able to see on `url/docs`. It is generated automatically by fastapi. It also provides API playground.

## useful link preferences

- stream communication: https://github.com/sysid/sse-starlette
