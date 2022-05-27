# Dockerfile

FROM python:3.10
WORKDIR /code

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

ENTRYPOINT ["./stream_video.py"]
