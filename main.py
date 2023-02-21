#!python3

import sys
import requests
import os
import json

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

if r.status_code != 200:
    print("ERROR: {0} {1}".format(r.status_code, str(r)))
    sys.exit(-1)
else:
    print("SUCCESS")
    sys.exit(0)
