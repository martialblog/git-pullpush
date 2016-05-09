#!/usr/bin/env python3

import tempfile
import unittest
import git
import os
import shutil

#import pullpush.pullpush as pp


class mockrepo:
    """
    Initializes a mock repo for the unittest.
    """

    TMP_DIR = tempfile.TemporaryDirectory(suffix='pullpush-unittest-repos')

    def __init__(self, function, reponame):
        self.function = function
        self.reponame = reponame

    def __call__(self):

        self.setup_mockrepo(self.reponame)
        self.function(self)
        self.remove_mockrepo(self.reponame)

    def setup_mockrepo(self, reponame):
        """
        Creates a test repo in the /tmp dir and commits an empty file.
        """

        repo_dir = os.path.join(mockrepo.TMP_DIR, reponame)
        file_name = os.path.join(repo_dir, 'test-file')

        repo = git.Repo.init(repo_dir)

        open(file_name, 'wb').close()
        repo.index.add([file_name])
        repo.index.commit("Initial Commit")

    def remove_mockrepo(self, reponame):
        """
        Removes a repository folder.
        """

        repo_dir = os.path.join(mockrepo.TMP_DIR, reponame)
        shutil.rmtree(repo_dir)

class PullPushTest(unittest.TestCase):
    """Some basic tests to check the PullPush class"""

    def setUp(self):
        pp = PullPush()

    #@mockrepo
    def test_pull(self):
        assert True

    #@mockrepo
    def test_push(self):
        assert True

    @mockrepo('set_target_repo')
    def test_set_target_repo(self):
        expected_repo_target = 'target'
        assert True
