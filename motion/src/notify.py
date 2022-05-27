#!/usr/bin/python3
# notify.py

import os
import sys
import json
import requests


def get_camera(camera_name):
    return camera_name.lower().replace(' ', '_')


if __name__ == '__main__':
    json_payload = {}
    for i in range(1, len(sys.argv)):
        if i == 3:
            json_payload['value3'] = os.environ['SITE_ROOT'] + f'/stream/{get_camera(sys.argv[i])}/'
        else:
            json_payload[f'value{i}'] = sys.argv[i]

    ifttt_webhooks = json.loads(os.environ['IFTTT_WEBHOOKS'])
    for ifttt_webhook in ifttt_webhooks:
        requests.post(ifttt_webhook, json=json_payload)
