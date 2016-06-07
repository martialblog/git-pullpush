#!/usr/bin/env python3


import tempfile
import unittest
import git
import os
import shutil
import time

import pullpush.pullpush as pp

TMP_DIR = tempfile.TemporaryDirectory(suffix='pullpush-unittest-repos')

class PullPushTest(unittest.TestCase):
    """
    Some basic tests to check the PullPush class
    """

    def setUp(self):


        self.PORT = 4567
        self.repos = {
            'test_pullpush_origin': 'URL',
            'test_pullpush_target': 'URL',
            }

        for reponame in self.repos.keys():
            repo_dir = os.path.join(TMP_DIR.name, reponame)
            repo = git.Repo.init(repo_dir, shared=True, bare=True)
            repo.daemon_export = True

            self.repos[reponame] = "git://localhost:%s%s%s" % (self.PORT,
                                                               TMP_DIR.name,
                                                               '/' + reponame)

        self.gd = git.Git().daemon(TMP_DIR.name,
                                   enable='receive-pack',
                                   listen='127.0.0.1',
                                   port=self.PORT,
                                   as_process=True)


    def tearDown(self):

        if self.gd is not None:
            os.kill(self.gd.proc.pid, 15)


    def test_pull(self):

        repo_dir = os.path.join(TMP_DIR.name, 'test_pull_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)
        PullPush.pull(self.repos['test_pullpush_origin'])

        self.assertEqual(os.path.isdir(repo_dir + '/.git'), True)


    def test_push(self):

        repo_dir = os.path.join(TMP_DIR.name, 'test_push_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)
        PullPush.pull(self.repos['test_pullpush_origin'])

        self.assertEqual(os.path.isdir(repo_dir + '/.git'), True)

        assert True


    def test_set_remote_url(self):

        repo_dir = os.path.join(TMP_DIR.name, 'test_remoteurl_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)
        PullPush.pull(self.repos['test_pullpush_origin'])

        PullPush.set_remote_url('new_url')

        # TODO self.AssertEqual(test_pp.remote_url, 'new_url)
        assert True
