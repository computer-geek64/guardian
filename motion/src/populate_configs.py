#!/usr/bin/python3 -B
# populate_configs.py

import os
import json
from subprocess import Popen, DEVNULL


def get_camera_name(camera):
    return ' '.join(word.capitalize() for word in camera.split('_'))


if __name__ == '__main__':
    rtsp_urls = json.loads(os.environ['RTSP_URLS'])

    for camera in rtsp_urls:
        filename = '/etc/motion/conf.d/{name}.conf'.format(name=camera)
        if os.path.exists(filename):
            if '@' in rtsp_urls[camera]:
                username, password = rtsp_urls[camera].split('rtsp://', 1)[1].split('@', 1)[0].split(':', 1)
                Popen(['sed', '-i', f's#{{{{USERNAME}}}}#{username}#;s#{{{{PASSWORD}}}}#{password}#', f'{filename}'], stdout=DEVNULL, stderr=DEVNULL).wait()
                rtsp_url_without_credentials = 'rtsp://' + rtsp_urls[camera].split('@', 1)[1]
            else:
                rtsp_url_without_credentials = rtsp_urls[camera]

            Popen(['sed', '-i', f's#{{{{RTSP_URL}}}}#{rtsp_url_without_credentials}#;s#{{{{CAMERA}}}}#{camera}#;s#{{{{NAME}}}}#{get_camera_name(camera)}#', f'{filename}'], stdout=DEVNULL, stderr=DEVNULL).wait()
        else:
            print(f'{filename} does not exist')

