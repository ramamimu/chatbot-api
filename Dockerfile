FROM python:3.8.10

WORKDIR /app

COPY requirements.txt /app/

# RUN pip install -r requirements.txt

RUN ls -a /app

COPY * /app/

EXPOSE 8000

CMD [ "fastapi", "run", "app.py" ]