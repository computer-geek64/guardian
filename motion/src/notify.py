#!/usr/bin/python3.8 -B
# notify.py

import os
import sys
import json
import requests


if __name__ == '__main__':
    json_payload = {}
    for i in range(1, len(sys.argv)):
        json_payload[f'value{i}'] = sys.argv[i]

    ifttt_webhooks = json.loads(os.environ['IFTTT_WEBHOOKS'])
    for ifttt_webhook in ifttt_webhooks:
        requests.post(ifttt_webhook, json=json_payload)
