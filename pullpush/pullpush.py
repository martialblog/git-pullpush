#!/usr/bin/env python3


import git


class PullPush:

    def __init__(self, repo_dir):
        self.repo_dir = repo_dir
        self.repo = None

    def pull(self, source_repo):
        """
        Pulls the remote source_repo and stores it in the repo_dir directory.
        """

        # TODO Better handling
        if not source_repo.startswith('git'):
            print("Invalid source repository url.")
            return

        self.repo = git.Repo.init(self.repo_dir)
        origin = self.repo.create_remote('origin', source_repo)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    def set_target_repo(self, new_url):
        """
        Changes the target url of the previously pulled repo.
        """

        origin = self.repo.remotes.origin
        cw = origin.config_writer
        cw.set("url", new_url)
        cw.release()

    def push(self, target_repo):
        """
        Pushes the previously pulled repo to the target_repo.
        """

        # TODO Better handling
        if self.repo is None:
            print("No source repository defined.")
            return

        if not new_url.startswith('git'):
            print("Invalid target repository url.")
            return

        origin = self.repo.remotes.origin
        self.set_target_repo(target_repo)
        self.repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
        origin.push()
