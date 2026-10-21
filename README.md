# make-jira-release

This action is for transitioning tickets from
MERGED to DEPLOYED and will be triggered from
release.yml github workflows.

You want the tickets in your release to all
be deployed otherwise the Jira release won't
be 'released', it'll be stuck in 'pre-release'
until all the tickets are at a terminus.

It's made to use the output from
https://github.com/fifthsun/get-tickets-in-release
which will automatically figure out that list.

## Usage

```
  - name: Make Jira release from tickets
    id: make-release
    uses: fifthsun/make-jira-release@main
    with:
      # OPTIONAL, will automatically be detected by default
      project: example

      # OPTIONAL, will automatically be detected by default
      release: v1.2.0

      # Organization wide secret
      webhook-url: ${{ secrets.JIRA_WEBHOOK_NEW_RELEASE }}

      # Space seperated list of tickets e.g. MEG-1023 MEG-2039, ...
      tickets: ${{ steps.get-tickets-in-release.outputs.tickets }}
```

## Image

`action.yml` runs a prebuilt, public image from GHCR
(`ghcr.io/fifthsun/make-jira-release`), pinned by digest. Callers pull it without logging
in, and nothing is built at run time, so no Docker Hub login or `id-token: write` is needed.
Before v2.3.0 the action built its Dockerfile on every run, and callers had to log into
Docker Hub first to avoid 429s. Callers on v2.3.0 can remove that login step.

## Publishing the image

`.github/workflows/publish-image.yml` builds and pushes the image whenever
`Dockerfile`, `main.py` or `requirements.txt` change on `main` (or on manual dispatch).
It tags the image `sha-<commit>` and `main`. To release a change:

1. Merge it to `main` and wait for `publish-image` to finish.
2. Copy the `image: docker://ghcr.io/fifthsun/make-jira-release@sha256:…` line from the
   run summary into `action.yml`. Pin the digest, not a tag: tags can be moved.
3. Merge that, then tag a release (`gh release create vX.Y.Z --target main`).

## Output

Prints `SUCCESS` when the Jira webhook accepts the release — any `2xx`,
including the `202 Accepted` that Jira Automation returns. With no tickets, it
skips and passes.

If the request errors or returns a non-`2xx`, it emits a GitHub Actions
`::warning::` annotation (including the status code and response body) and
still exits `0` — so a Jira problem is visible in the run summary but never
fails an already-completed deploy.
