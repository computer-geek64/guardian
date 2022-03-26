# Dockerfile
FROM nginx/unit:1.26.1-python3.10

WORKDIR /code
RUN apt-get update
RUN apt-get install -y uuid-runtime ffmpeg

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

RUN cp config.json /docker-entrypoint.d/

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
