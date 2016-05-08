#!/usr/bin/env python3


import unittest
import git
import os
import shutil

import pullpush.pullpush as pp


class mockrepos:
    """
    Initializes mock repos for the unittest.
    """

    tmp_dir = '/tmp/pullpush-unittest-repos/'

    def __init__(self, function):
        self.function = function

    def __call__(self):

        self.setup_mockrepo('source_repo')
        self.setup_mockrepo('target_repo')

        self.function(self)

        self.remove_mockrepo('source_repo')
        self.remove_mockrepo('target_repo')

    def setup_mockrepo(self, reponame):
        """
        Creates a test repo in the /tmp dir and commits an empty file.
        """

        repo_dir = os.path.join(mockrepos.tmp_dir, reponame)
        file_name = os.path.join(repo_dir, 'test-file')

        repo = git.Repo.init(repo_dir)

        open(file_name, 'wb').close()
        repo.index.add([file_name])
        repo.index.commit("Initial Commit")

    def remove_mockrepo(self, reponame):
        """
        Removes a repository folder.
        """

        repo_dir = os.path.join(mockrepos.tmp_dir, reponame)
        shutil.rmtree(repo_dir)

class PullPush(unittest.TestCase):
    """Some basic tests to check the PullPush class"""

    def setUp(self):
        pass

    @mockrepos
    def test_pull(self):
        assert True

    @mockrepos
    def test_push(self):
        assert True

    def test_set_target_repo(self):
        assert True
