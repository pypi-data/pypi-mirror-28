# Slack Releaser Utility

A simple utility that posts release changelogs to a configured Slack Webhook.

## Usage

Install `slack-releaser` from PyPI:

```
pip install slack-releaser
```

Add the following to your `setup.cfg`:

```ini
[zest.releaser]
prereleaser.after =
  slack_releaser.releaser.post_to_slack

[slack.releaser]

webhook = https://example.slack.com/hook/abc123
repository = https://github.com/example/repository
```

Replace `webhook` with the webhook URL that Slack gives you when you setup a
webhook.

See the [Slack Documentation](https://api.slack.com/custom-integrations/incoming-webhooks)
for help in setting up webhooks.

## License

[MIT License](./LICENSE)
