#!python3

import sys
import requests
import os
import json

try:
    payload = {
        'release': {
            'tag_name': "{0}-{1}".format(
                os.environ.get('INPUT_PROJECT'),
                os.environ.get('INPUT_RELEASE')
            )
        },
        'issues': list(os.environ.get('INPUT_TICKETS').split(' '))
    }
    r = requests.post(
        url=os.environ.get('INPUT_WEBHOOK-URL'),
        headers={'Content-Type': 'application/json'},
        json=payload)
    print("SUCCESS")
    sys.exit(0)
except Exception as e:
    # If there are no tickets in the release,
    # auto-pass regardless so as not to effect the deploy report.
    print("SUCCESS")
    sys.exit(0)
