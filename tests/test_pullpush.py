#!/usr/bin/env python3

import tempfile
import unittest
import git
import os
import shutil

#import pullpush.pullpush as pp


class mockrepos:
    """
    Initializes a mock repo for the unittest.
    """

    TMP_DIR = tempfile.TemporaryDirectory(suffix='pullpush-unittest-repos')

    def __init__(self, function, *repo):
        self.function = function
        self.repos = repo

    def __call__(self):

        self.setup_mockrepos()
        self.function(self)
        self.teardown_mockrepos(self.reponame)

    def create_repo(self, reponame):
        """
        Creates a test repo in the /tmp dir and commits an empty file.
        """

        repo_dir = os.path.join(mockrepo.TMP_DIR, reponame)
        file_name = os.path.join(repo_dir, 'test-file')
        repo = git.Repo.init(repo_dir)

        #TODO Maybe move to own funtion
        open(file_name, 'wb').close()
        repo.index.add([file_name])
        repo.index.commit("Initial Commit")

    def remove_repo(self, reponame):
        """
        Removes a repository folder.
        """

        repo_dir = os.path.join(mockrepo.TMP_DIR, reponame)
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
    """Some basic tests to check the PullPush class"""

    def setUp(self):

    #@mockrepo
    def test_pull(self):
        assert True

    #@mockrepo
    def test_push(self):
        assert True

    @mockrepos('set_target_repo')
    def test_set_target_repo(self):

        #pp = PullPush() # TODO need to get the path to mockrepo
        #expected_repo_target = 'target'
        #pp.set_target_repo(expected_repo_target)

        assert True
