#!/usr/local/bin/python
# stream_video.py

import os
import cv2
import json
import redis
from time import sleep
from datetime import datetime, timedelta


def publish_video_streams(fps=10):
    streams = {camera: cv2.VideoCapture(rtsp_urls[camera]) for camera in rtsp_urls}

    last_read = datetime.now() - timedelta(seconds=1)

    while not redis_client.exists('pause_streams') or redis_client.get('pause_streams').decode() != '1':
        while last_read >= datetime.now() - timedelta(seconds=1 / fps):
            sleep(0.01)
            for camera in streams:
                streams[camera].grab()

        for camera in streams:
            read_success, frame = streams[camera].read()

            # Raw
            ret, buffer = cv2.imencode('.jpg', frame)
            redis_client.publish(f'{camera}_video_stream_raw', buffer.tobytes())

            # HD
            if frame.shape[0] // 3 == frame.shape[1] // 4:
                frame = cv2.resize(frame, (1280, 960))  # 4:3
            else:
                frame = cv2.resize(frame, (1280, 720))  # 16:9
            ret, buffer = cv2.imencode('.jpg', frame)
            redis_client.publish(f'{camera}_video_stream_hd', buffer.tobytes())

            # SD
            if frame.shape[0] // 3 == frame.shape[1] // 4:
                frame = cv2.resize(frame, (640, 480))  # 4:3
            else:
                frame = cv2.resize(frame, (640, 360))  # 16:9
            ret, buffer = cv2.imencode('.jpg', frame)
            redis_client.publish(f'{camera}_video_stream_sd', buffer.tobytes())

        last_read = datetime.now()

    for camera in streams:
        streams[camera].release()


if __name__ == '__main__':
    rtsp_urls = json.loads(os.environ['RTSP_URLS'])

    redis_client = redis.Redis(host='redis')

    while True:
        publish_video_streams()

        while not redis_client.exists('pause_streams') or redis_client.get('pause_streams').decode() == '1':
            sleep(3)
