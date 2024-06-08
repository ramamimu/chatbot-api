FROM python:3.8.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    iputils-ping \
    curl \
    netcat

RUN ls -a /app

ENV PGUSER=postgres
ENV PGHOST=postgres-chatbot
ENV PGPASSWORD=postgres
ENV PGDATABASE=chatbot
ENV PGPORT=5432

RUN python3 model.download.py
RUN python3 embed.init.py

EXPOSE 5000

CMD [ "make", "start-deploy"]