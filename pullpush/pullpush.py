#!/usr/bin/env python3


import git
import tempfile
from argparse import ArgumentParser


class PullPush:

    def __init__(self, source_repo, target_repo, repo_dir):
        self.source_repo = source_repo
        self.target_repo = target_repo
        self.repo_dir = repo_dir
        self.repo = None

    def pull(self):
        """
        Pulls the source_repo and stores it in a directory.
        """

        self.repo = git.Repo.init(self.repo_dir)
        origin = self.repo.create_remote('origin', self.source_repo)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    def set_target_repo(self, new_url):
        """
        Changes the target url.
        """

        origin = self.repo.remotes.origin
        cw = origin.config_writer
        cw.set("url", new_url)
        cw.release()

    def push(self):
        """
        Pushes the repo to the new remote url.
        """

        origin = self.repo.remotes.origin
        self.set_target_repo(self.target_repo)
        self.repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
        origin.push()


def main():

    description = "Pull a git repository, pushes it somewhere and tells Slack about it"

    #Parsing Command-Line Arguments
    argumentparser = ArgumentParser(description=description)
    argumentparser.add_argument('pull_from', help='The repo to pull from')
    argumentparser.add_argument('push_into', help='The repo to push into')

    cmd_arguments = argumentparser.parse_args()
    pull_from = cmd_arguments.pull_from
    push_into = cmd_arguments.push_into

    #Just for testing since I'm too lazy to type/paste
    pull_from = "https://github.com/martialblog/www-zweipunknull.git"
    push_into = 'http://127.0.0.1:4567/root/zweipunknull.git'

    with tempfile.TemporaryDirectory() as temporary_dir:
        pp = PullPush(source_repo=pull_from, target_repo=push_into, repo_dir=temporary_dir)
        pp.pull()
        pp.push()


if __name__ == "__main__":
    main()
