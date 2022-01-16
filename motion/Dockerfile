# Dockerfile
FROM ubuntu:latest

WORKDIR /code
RUN apt-get update
RUN apt-get install -y motion curl python3.8

COPY src .
RUN cp motion.conf /etc/motion/motion.conf
RUN mkdir -p /etc/motion/conf.d
RUN cp backyard_camera.conf /etc/motion/conf.d/backyard_camera.conf

ENTRYPOINT ["./init.sh"]
