FROM python:3.8.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt


COPY * /app/

EXPOSE 8000

CMD [ "fastapi", "run", "app.py" ]