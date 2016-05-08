#!/usr/bin/env python3


import git


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
