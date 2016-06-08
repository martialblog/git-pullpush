#!/usr/bin/env python3
# TODO Slack Integration
# TODO Retry-If-Fail implementation


from tempfile import TemporaryDirectory
from argparse import ArgumentParser
from pullpush import PullPush


DESC = 'Pulls a git repository and pushes it somewhere'
HELP_PULL = 'The repo to pull from'
HELP_PUSH = 'The repo to push into'


def main():

    argumentparser = ArgumentParser(description=DESC)
    argumentparser.add_argument('--from', dest='pullfrom', required=True, help=HELP_PULL)
    argumentparser.add_argument('--into', dest='pushto', required=True, help=HELP_PUSH)

    cmd_arguments = argumentparser.parse_args()

    origin = cmd_arguments.pullfrom
    target = cmd_arguments.pushto

    with TemporaryDirectory() as temp_dir:
        pp = PullPush(repo_dir=temp_dir)
        pp.pull(origin)
        pp.push(target)


if __name__ == "__main__":
    main()
