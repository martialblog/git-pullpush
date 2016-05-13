#!/usr/bin/env python3
# TODO Test if different branch names make trouble


import git


class PullPush:

    def __init__(self, repo_dir):
        """
        Arguments:
        repo_dir -- Directory in which to pull into
        """

        self.repo_dir = repo_dir
        self.repo = None

    def pull(self, source_repo):
        """
        Pulls from a remote repository and stores it in the directory.

        Arguments:
        source_repo -- URL of the remote git repository
        """

        #TODO Catch possible exceptions: source_repo not defined
        self.repo = git.Repo.init(self.repo_dir)
        origin = self.repo.create_remote('origin', source_repo)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

    def set_target_repo(self, new_url):
        """
        Changes the target url of the previously pulled repo.

        Arguments:
        new_url -- New remote url of the repository
        """

        #TODO Catch possible exceptions: Repo not initialized
        origin = self.repo.remotes.origin
        cw = origin.config_writer
        cw.set("url", new_url)
        cw.release()

    def push(self, target_repo):
        """
        Pushes the previously pulled repo to the target repository.

        Arguments:
        target_repo: Url of the target remote repository
        """

        #TODO Catch possible exceptions: Repo not initialized
        origin = self.repo.remotes.origin
        self.set_target_repo(target_repo)
        self.repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
        origin.push()
