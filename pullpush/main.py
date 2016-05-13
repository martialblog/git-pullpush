#!/usr/bin/env python3
# TODO Deploy Key Integration
# TODO Slack Integration
# TODO Error/Expection Handling
# TODO Retry-If-Fail implementation


import tempfile
from argparse import ArgumentParser
from pullpush import PullPush


def main():

    description = "Pull a git repository, pushes it somewhere"

    #Parsing Command-Line Arguments
    argumentparser = ArgumentParser(description=description)
    argumentparser.add_argument('pull_from', help='The repo to pull from')
    argumentparser.add_argument('push_into', help='The repo to push into')

    cmd_arguments = argumentparser.parse_args()

    pull_from = cmd_arguments.pull_from
    push_into = cmd_arguments.push_into

    with tempfile.TemporaryDirectory() as temporary_dir:
        pp = PullPush(repo_dir=temporary_dir)
        pp.pull(pull_from)
        pp.push(push_into)


if __name__ == "__main__":
    main()
