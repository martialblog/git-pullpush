#!/usr/bin/env python3


import tempfile
import time
import unittest
import git
import os
import pullpush.pullpush as pp

# Needs to be here cause of scope
TMP_DIR = tempfile.TemporaryDirectory(suffix='pullpush-unittest-repos')

class PullPushTest(unittest.TestCase):
    """
    Some basic tests to check the PullPush class
    """

    def create_repodir(self, name):

        repo_dir = os.path.join(TMP_DIR.name, name)
        repo = git.Repo.init(repo_dir, shared=True, bare=True)
        repo.daemon_export = True


    def git_daemon(self, _port, _basedir):

        gd = git.Git().daemon(_basedir,
                              enable='receive-pack',
                              listen='127.0.0.1',
                              port=_port,
                              as_process=True)

        return gd


    def setUp(self):

        # TODO Some stuff can probably moved to own function
        self.PORT = 4567
        self.repos = {
            'test_pullpush_origin': 'URL',
            'test_pullpush_target': 'URL',
            }

        for reponame in self.repos.keys():
            self.create_repodir(reponame)
            self.repos[reponame] = "git://localhost:%s%s%s" % (self.PORT,
                                                               TMP_DIR.name,
                                                               '/' + reponame)

        self.gd = self.git_daemon(self.PORT, TMP_DIR.name)
        # Sometimes I think the daemon doesn't start propertly
        time.sleep(2)


    def tearDown(self):

        if self.gd is not None:
            os.kill(self.gd.proc.pid, 15)


    def test_pull(self):

        repo_dir = os.path.join(TMP_DIR.name, 'test_pull_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)
        PullPush.pull(self.repos['test_pullpush_origin'])
        was_pulled = os.path.isdir(repo_dir + '/.git')

        self.assertEqual(was_pulled, True)


    def test_set_remote_url(self):

        expected_url = 'unittest_url'
        repo_dir = os.path.join(TMP_DIR.name, 'test_remoteurl_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)

        PullPush.pull(self.repos['test_pullpush_origin'])
        PullPush.set_remote_url(expected_url)

        origin = PullPush.repo.remotes.origin
        cr = origin.config_reader
        actual_url = cr.get_value('url')

        self.assertEqual(actual_url, expected_url)


    def test_push(self):

        repo_dir = os.path.join(TMP_DIR.name, 'test_push_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)

        PullPush.pull(self.repos['test_pullpush_origin'])

        # # Need a commit of we cant push
        tmpfile = tempfile.NamedTemporaryFile(dir=repo_dir)
        index = PullPush.repo.index
        index.add([tmpfile.name])
        index.commit('Unittest Commit')

        PullPush.push(self.repos['test_pullpush_target'])

        #TODO
        was_pushed = os.path.isfile('...')

        self.assertEqual(was_pushed, True)
