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

## Output

Prints `SUCCESS` when the Jira webhook accepts the release — any `2xx`,
including the `202 Accepted` that Jira Automation returns. With no tickets, it
skips and passes.

If the request errors or returns a non-`2xx`, it emits a GitHub Actions
`::warning::` annotation (including the status code and response body) and
still exits `0` — so a Jira problem is visible in the run summary but never
fails an already-completed deploy.
