#!/usr/bin/env python3


import tempfile
import unittest
import git
import os
import shutil


class mockrepo:
    """
    Initializes a mock repo for the unittest.
    """

    GIT_DAEMON_PORT = 4567
    TMP_DIR = tempfile.TemporaryDirectory(suffix='pullpush-unittest-repos')


    def __init__(self, *repo):
        self.repos = repo
        self.gd = git.Git().daemon(mockrepo.TMP_DIR.name,
                                   enable='receive-pack',
                                   listen='127.0.0.1',
                                   port=mockrepo.GIT_DAEMON_PORT,
                                   as_process=True)

    def __call__(self, func):

        def wrapper(*args):
            self.setup_mockrepos()
            func(*args)
            self.teardown_mockrepos()

        return wrapper

    def create_repo(self, reponame):
        """
        Creates a test repo in the /tmp dir and commits an empty file.
        """

        repo_dir = os.path.join(mockrepo.TMP_DIR.name, reponame)
        repo = git.Repo.init(repo_dir, shared=True, bare=True)
        repo.daemon_export = True

        # TODO Commit test file to repo

    def remove_repo(self, reponame):
        """
        Removes a repository folder.
        """

        repo_dir = os.path.join(mockrepo.TMP_DIR.name, reponame)
        shutil.rmtree(repo_dir)


    def setup_mockrepos(self):
        """
        Creates all the desired repos.
        """

        for reponame in self.repos:
            self.create_repo(reponame)


    def teardown_mockrepos(self):

        if self.gd is not None:
            os.kill(self.gd.proc.pid, 15)

        for reponame in self.repos:
            self.remove_repo(reponame)


class PullPushTest(unittest.TestCase):
    """
    Some basic tests to check the PullPush class
    """

    @mockrepo('repo1', 'repo2')
    def test_pull(self):

        repo_dir = os.path.join(mockrepo.TMP_DIR.name, 'something')
        remote_repo_url = "git://127.0.0.1:%s%s%s" % (mockrepo.GIT_DAEMON_PORT,
                                                      mockrepo.TMP_DIR.name,
                                                      '/repo1')

        git.Repo.clone_from(remote_repo_url, repo_dir)

        assert True


    def test_push(self):
        assert True


    def test_set_remote_url(self):
        assert True
