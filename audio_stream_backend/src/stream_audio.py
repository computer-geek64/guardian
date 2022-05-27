#!/usr/local/bin/python
# stream_audio.py

import os
import json
import redis
import signal
from time import sleep
from subprocess import Popen, PIPE, DEVNULL


def publish_audio_streams():
    processes = {camera: Popen(['ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_urls[camera], '-vn', '-f', 'mp3', 'pipe:stdout'], stdout=PIPE, stderr=DEVNULL) for camera in rtsp_urls}

    while not redis_client.exists('pause_streams') or redis_client.get('pause_streams').decode() != '1':
        for camera in processes:
            data = processes[camera].stdout.read(1024)
            redis_client.publish(f'{camera}_audio_stream', data)

    for camera in processes:
        processes[camera].send_signal(signal.SIGKILL)


if __name__ == '__main__':
    rtsp_urls = json.loads(os.environ['RTSP_URLS'])

    redis_client = redis.Redis(host='redis')

    while True:
        publish_audio_streams()

        while not redis_client.exists('pause_streams') or redis_client.get('pause_streams').decode() == '1':
            sleep(3)
