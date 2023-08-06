"""Release functions.
"""
from __future__ import absolute_import, print_function, unicode_literals

import configparser
import getpass
import re

from os import path

import requests

from .exceptions import ConfigError, RequestError

VERSION_REGEX = re.compile(r'\s\d+\.\d+\.\d+\s')

SETUP_CONFIG_HELP = '''Your setup.cfg file must contain the following info:

[slack.releaser]
webhook = <slack_webhook>
repository = <link_to_repository>

For example:

[slack.releaser]
webhook = https://example.slack.com/hook/abc123
repository = https://github.com/mypebble/slack-releaser
'''


def post_to_slack(data):
    """Post the new changelog information to Slack.

    This takes the version history and splits based on where the version number
    is located. This then takes the entire content between the two locations
    and sends that data up to the specified Slack channel.
    """
    app_name = data['name']
    version = data['new_version']
    major, minor, patch = version.split('.')
    search_lines = [line for line in data['history_lines'][1:]]
    user = getpass.getuser()

    config = configparser.ConfigParser()

    read_files = config.read(path.join(data['workingdir'], 'setup.cfg'))
    if not read_files:
        raise ConfigError('You must have a setup.cfg file.\n\n{}'.format(
            SETUP_CONFIG_HELP))

    if 'slack.releaser' not in config:
        message = 'Your setup.cfg file must contain'
        raise ConfigError(
            'slack.releaser not configured in setup.cfg.\n\n{}'.format(
                SETUP_CONFIG_HELP))
    else:
        options = config['slack.releaser']

    webhook = options['webhook']
    repo = options['repository']

    tag_url = '{}/tree/{}'.format(repo, version)

    end = len(search_lines) - 1

    for i, line in enumerate(search_lines):
        if line.startswith('#') or VERSION_REGEX.findall(line):
            end = i
            break

    changelog = '\n'.join(s for s in search_lines[:end] if s)

    payload = {
        'attachments': [
            {
                'fallback': _get_fallback_string(app_name, version, changelog,
                                                 tag_url),
                'color': '#228b22',
                'author_name': user,
                'title': 'Release {} - {}'.format(app_name, version),
                'pretext': 'Build Released',
                'title': '{} {}'.format(app_name, version),
                'title_link': tag_url,

                'fields': [
                    {
                        'title': 'Release contains',
                        'value': changelog,
                        'short': False,
                    }
                ]}
        ]
    }
    ret = requests.post(webhook, json=payload)

    try:
        ret.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        if ret.status_code in (400, 500):
            error_text = ('Slack returned the following error code: {code} '
                          'and message: {message}'.format(
                              code=ret.status_code,
                              message=exc.text))
            raise ConfigError(error_text)
        else:
            print('Could not sent to Slack. Continuing release.')


def _get_fallback_string(app_name, version, changelog, tag_url):
    """Return the Fallback String.
    """
    return '''# {app}

**Url** <{url}>
# {version}

{changes}'''.format(app=app_name, version=version, changes=changelog,
                    url=tag_url)
