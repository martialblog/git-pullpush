#!/usr/bin/env python3


import git


class PullPush:


    def __init__(self, repo_dir):
        """
        :param repo_dir: Directory in which to pull into
        """

        self.repo_dir = repo_dir
        self.repo = None


    def pull(self, origin):
        """
        Pulls from a remote repository and stores it in the directory.
        :param origin: URL of the remote git repository
        """

        #TODO Catch possible exceptions: source_repo not defined
        self.repo = git.Repo.clone_from(origin, self.repo_dir)


    def set_remote_url(self, new_url):
        """
        Changes the target url of the previously pulled repo.
        :param new_url: New remote url of the repository
        """

        #TODO Catch possible exceptions: Repo not initialized
        origin = self.repo.remotes.origin
        cw = origin.config_writer
        cw.set("url", new_url)
        cw.release()


    def push(self, target):
        """
        Pushes the previously pulled repo to the target repository.
        :param target_repo: Url of the target remote repository
        """

        #TODO Catch possible exceptions: Repo not initialized
        self.set_remote_url(target)
        self.repo.git.push('--all')
