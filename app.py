#!python3

import json
import os
import sys
import requests

# Our arguments are release name and an array of tickets.
# Generate our payload

payload = {
    'release': {
        'tag_name': sys.argv[2] # First argument is our release name
    },
    'issues': sys.argv[3:]      # Everything else is treated as a ticket
}

r = requests.post(
              url=sys.argv[1],
              headers={'Content-Type': 'application/json'}, 
              json=payload)

if r.status_code != 200:
    print("ERROR: {0} {1}".format(r.status_code, str(r)))
    sys.exit(-1)
else:
    print("SUCCESS")
    sys.exit(0)
