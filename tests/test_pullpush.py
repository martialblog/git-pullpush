#!/usr/bin/env python3


import tempfile
import unittest
import git
import os
import shutil
import time
import pullpush.pullpush as pp


TMP_DIR = tempfile.TemporaryDirectory(suffix='pullpush-unittest-repos')
GIT_DAEMON_PORT = 4567


class mockrepo:
    """
    Initializes a mock repo for the unittest.
    """

    def __init__(self, repo_dir, *repo):
        self.repos = repo
        self.repo_dir = repo_dir


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

        repo_dir = os.path.join(self.repo_dir, reponame)
        repo = git.Repo.init(repo_dir, shared=True, bare=True)
        repo.daemon_export = True

        # TODO Commit test file to repo


    def remove_repo(self, reponame):
        """
        Removes a repository folder.
        """

        repo_dir = os.path.join(self.repo_dir)
        shutil.rmtree(repo_dir)


    def setup_mockrepos(self):
        """
        Creates all the desired repos.
        """

        for reponame in self.repos:
            self.create_repo(reponame)


    def teardown_mockrepos(self):

        for reponame in self.repos:
            self.remove_repo(reponame)


class PullPushTest(unittest.TestCase):
    """
    Some basic tests to check the PullPush class
    """

    def setUp(self):

        self.gd = git.Git().daemon(TMP_DIR.name,
                                   enable='receive-pack',
                                   listen='127.0.0.1',
                                   port=GIT_DAEMON_PORT,
                                   as_process=True)


    def tearDown(self):

        if self.gd is not None:
            os.kill(self.gd.proc.pid, 15)


    @mockrepo(TMP_DIR.name, 'test_pull_repo')
    def test_pull(self):

        repo_dir = os.path.join(TMP_DIR.name, 'test_pull')
        remote_repo_url = "git://localhost:%s%s%s" % (GIT_DAEMON_PORT,
                                                      TMP_DIR.name,
                                                      '/test_pull_repo')


        pull = pp.PullPush(repo_dir=repo_dir)
        pull.pull(remote_repo_url)

        self.assertEqual(os.path.isdir(repo_dir + '/.git'), True)


    @mockrepo('test_push_repo1', 'test_push_repo2')
    def test_push(self):

        assert True


    @mockrepo('test_url')
    def test_set_remote_url(self):

        repo_dir = os.path.join(mockrepo.TMP_DIR.name, 'test_remote_url')
        print(os.path.isdir(mockrepo.TMP_DIR.name))
        remote_repo_url = "git://localhost:%s%s%s" % (mockrepo.GIT_DAEMON_PORT,
                                                      mockrepo.TMP_DIR.name,
                                                      '/test_url')

        test_pp = pp.PullPush(repo_dir=repo_dir)
        test_pp.pull(remote_repo_url)
        test_pp.set_remote_url('new_url')

        # TODO self.AssertEqual(test_pp.remote_url, 'new_url)
        assert True
