#!/usr/bin/env python3
# TODO Deploy Key Integration
# TODO Slack Integration
# TODO Error/Expection Handling


import tempfile
from argparse import ArgumentParser
from pullpush import PullPush


def main():

    description = "Pull a git repository, pushes it somewhere and tells Slack about it"

    #Parsing Command-Line Arguments
    argumentparser = ArgumentParser(description=description)
    argumentparser.add_argument('pull_from', help='The repo to pull from')
    argumentparser.add_argument('push_into', help='The repo to push into')

    cmd_arguments = argumentparser.parse_args()
    pull_from = cmd_arguments.pull_from
    push_into = cmd_arguments.push_into

    with tempfile.TemporaryDirectory() as temporary_dir:
        pp = PullPush(source_repo=pull_from, target_repo=push_into, repo_dir=temporary_dir)
        pp.pull()
        pp.push()


if __name__ == "__main__":
    main()
