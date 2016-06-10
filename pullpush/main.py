#!/usr/bin/env python3
# TODO Retry-If-Fail implementation


from tempfile import TemporaryDirectory
from argparse import ArgumentParser
from slacker import Slacker
from pullpush import PullPush
from sys import exit


DESC = 'Pulls a git repository and pushes it somewhere'
HELP_PULL = 'The repo to pull from'
HELP_PUSH = 'The repo to push into'
API_TOKEN = 'TOKEN'
CHANNEL = '#puppet'

Slack = Slacker(API_TOKEN)


def notify(message, severity):
    """
    Wrapper for Slack notifications.
    """

    ICON = {
        'INFO', ':page_with_curl:',
        'WARN', ':warning:',
        'ERROR', ':bangbang:',
        '*', ':slack:'
    }

    msg = '{0} {1}'.format(ICON[severity], message)
    Slack.chat.post_message(CHANNEL, msg)


def main():

    argumentparser = ArgumentParser(description=DESC)
    argumentparser.add_argument('--from', dest='pullfrom', required=True, help=HELP_PULL)
    argumentparser.add_argument('--into', dest='pushto', required=True, help=HELP_PUSH)

    cmd_arguments = argumentparser.parse_args()

    origin = cmd_arguments.pullfrom
    target = cmd_arguments.pushto

    with TemporaryDirectory() as temp_dir:
        pp = PullPush(repo_dir=temp_dir)
        try:
            pp.pull(origin)
            pp.push(target)
            notify(message="All's good", severity='INFO')
        except Exception:
            notify(message="Something is wrong", severity='ERROR')
            exit(1)


if __name__ == "__main__":
    main()
    exit(0)
