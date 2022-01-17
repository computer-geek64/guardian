# Dockerfile
FROM ubuntu:latest

WORKDIR /code
RUN apt-get update
RUN apt-get install -y motion curl python3.8

RUN python3.8 -m pip install --upgrade pip

COPY requirements.txt .
RUN python3.8 -m pip install -r requirements.txt

COPY src .
RUN cp motion.conf /etc/motion/motion.conf
RUN mkdir -p /etc/motion/conf.d
RUN cp backyard_camera.conf /etc/motion/conf.d/backyard_camera.conf

ENTRYPOINT ["./init.sh"]
