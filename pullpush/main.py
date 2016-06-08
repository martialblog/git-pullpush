#!/usr/bin/env python3
# TODO Deploy Key Integration
# TODO Slack Integration
# TODO Error/Expection Handling
# TODO Retry-If-Fail implementation


import tempfile
from argparse import ArgumentParser
from pullpush import PullPush


DESC = 'Pulls a git repository and pushes it somewhere'


def main():

    argumentparser = ArgumentParser(description=DESC)
    argumentparser.add_argument('--from', dest='pullfrom', required=True, help='The repo to pull from')
    argumentparser.add_argument('--into', dest='pushto', required=True, help='The repo to push into')

    cmd_arguments = argumentparser.parse_args()

    origin = cmd_arguments.pullfrom
    target = cmd_arguments.pushto

    with tempfile.TemporaryDirectory() as temp_dir:
        pp = PullPush(repo_dir=temp_dir)
        pp.pull(origin)
        pp.push(target)


if __name__ == "__main__":
    main()
