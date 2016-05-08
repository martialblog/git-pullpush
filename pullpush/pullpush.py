#!/usr/bin/env python3


import git
import tempfile
from argparse import ArgumentParser

class PullPush:

    def __init__(self, source_repo, target_repo, tmpdir):
        self.source_repo = source_repo
        self.target_repo = target_repo
        self.tmpdir = tmpdir
        self.repo = None

    def pull(self):
        self.repo = git.Repo.init(self.tmpdir)
        origin = self.repo.create_remote('origin', self.source_repo)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    def push(self):
        origin = self.repo.remotes.origin

        cw = origin.config_writer
        cw.set("url", self.target_repo)
        cw.release()

        self.repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
        origin.push()


def main():

    description = "Pull a git repository, pushes it somewhere and tells Slack about it"
    argumentparser = ArgumentParser(description=description)
    argumentparser.add_argument('pull_from', help='The repo to pull from')
    argumentparser.add_argument('push_into', help='The repo to push into')


    cmd_arguments = argumentparser.parse_args()
    pull_from = cmd_arguments.pull_from
    push_into = cmd_arguments.push_into

    ############Testing############
    pull_from = "https://github.com/martialblog/www-zweipunknull.git"
    push_into = 'http://127.0.0.1:4567/root/zweipunknull.git'
    ###############################

    with tempfile.TemporaryDirectory() as tmpdirname:
        pp = PullPush(source_repo=pull_from, target_repo=push_into, tmpdir=tmpdirname)
        pp.pull()
        pp.push()


if __name__ == "__main__":
    main()
