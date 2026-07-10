#!python3

import os
import sys

import requests

WEBHOOK_URL = os.environ.get("INPUT_WEBHOOK-URL")
PROJECT = os.environ.get("INPUT_PROJECT") or ""
RELEASE = os.environ.get("INPUT_RELEASE") or ""
TICKETS = [t for t in (os.environ.get("INPUT_TICKETS") or "").split(" ") if t]

REQUEST_TIMEOUT_SECONDS = 30


def warn(message):
    # GitHub Actions warning annotation: visible in the run summary/UI
    # without failing the job. Workflow commands are single-line, so encode
    # control chars (a multi-line body such as an HTML 404 page would
    # otherwise break the annotation and drop the message). Encode '%' first.
    safe = (
        str(message)
        .replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
    )
    print("::warning title=Jira release::{0}".format(safe))


# Nothing to send: a release with no tickets is normal (e.g. infra-only
# releases). Pass so the deploy report isn't affected.
if not TICKETS:
    print("No Jira tickets in this release; nothing to send. Skipping.")
    sys.exit(0)

if not WEBHOOK_URL:
    warn("INPUT_WEBHOOK-URL is empty; cannot notify Jira. Skipping.")
    sys.exit(0)

payload = {
    "release": {"tag_name": "{0}-{1}".format(PROJECT, RELEASE)},
    "issues": TICKETS,
}

try:
    response = requests.post(
        url=WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
except requests.RequestException as error:
    # A Jira hiccup must never fail an already-completed deploy; surface it
    # loudly instead of silently passing.
    warn("Request to the Jira webhook failed: {0}".format(error))
    sys.exit(0)

# Jira Automation incoming webhooks return 202 Accepted, so accept any 2xx.
if 200 <= response.status_code < 300:
    print(
        "SUCCESS: Jira webhook accepted release {0}-{1} ({2})".format(
            PROJECT, RELEASE, response.status_code
        )
    )
    sys.exit(0)

# Non-2xx: make it obvious (this is how the stale JIRA_WEBHOOK_NEW_RELEASE
# secret would show up), but don't block the release job.
body = (response.text or "").strip()[:500]
warn(
    "Jira webhook returned {0}; release notes may not have been created. "
    "Response: {1}".format(response.status_code, body)
)
sys.exit(0)
