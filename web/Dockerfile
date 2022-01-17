# Dockerfile
FROM python:3.10

WORKDIR /code
RUN apt-get update
RUN apt-get install -y uuid-runtime ffmpeg

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY src .

ENTRYPOINT ["./server.py"]
