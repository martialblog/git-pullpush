#!/usr/bin/env python3


import tempfile
import time
import unittest
import git
import os
import pullpush.pullpush as pp
import shutil


TMP_DIR = tempfile.mkdtemp(suffix='pullpush-unittest-repos')
PORT = 4567


# TODO
# Sometime the gd doesn't seem to serve the repos
# I have no idea why! -.-
# Must have something to do with the time cause if I wait a bit (60sec) it works
time.sleep(60)

gd = git.Git().daemon(TMP_DIR,
                      enable='receive-pack',
                      listen='127.0.0.1',
                      port=PORT,
                      as_process=True)


class PullPushTest(unittest.TestCase):
    """
    Some basic tests to check the PullPush class
    """

    def create_repodir(self, name):

        repo_dir = os.path.join(TMP_DIR, name)
        repo = git.Repo.init(repo_dir, shared=True, bare=True)
        repo.daemon_export = True


    def setUp(self):

        self.repos = {
            'test_pullpush_origin': 'URL',
            'test_pullpush_target': 'URL',
            }

        for reponame in self.repos.keys():
            self.create_repodir(reponame)
            self.repos[reponame] = "git://localhost:%s%s%s" % (PORT,
                                                               TMP_DIR,
                                                               '/' + reponame)

    def tearDown(self):

        shutil.rmtree(TMP_DIR)


    def test_pull(self):
        """
        We test if an empty directory has a .git directory after the pull.
        """

        repo_dir = os.path.join(TMP_DIR, 'test_pull_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)
        PullPush.pull(self.repos['test_pullpush_origin'])

        was_pulled = os.path.isdir(repo_dir + '/.git')
        self.assertEqual(was_pulled, True)


    def test_set_remote_url(self):
        """
        We pull a repo, change the remote url and see if it got changed.
        """

        expected_url = 'unittest_url'
        repo_dir = os.path.join(TMP_DIR, 'test_remoteurl_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)

        PullPush.pull(self.repos['test_pullpush_origin'])
        PullPush.set_remote_url(expected_url)

        origin = PullPush.repo.remotes.origin
        cr = origin.config_reader
        actual_url = cr.get_value('url')

        self.assertEqual(actual_url, expected_url)


    def test_push(self):
        """
        We push a file to a target repo and see if it's there.
        """

        repo_dir = os.path.join(TMP_DIR, 'test_push_repo')
        PullPush = pp.PullPush(repo_dir=repo_dir)

        PullPush.pull(self.repos['test_pullpush_origin'])

        tmpfile = tempfile.NamedTemporaryFile(dir=repo_dir)
        index = PullPush.repo.index
        index.add([tmpfile.name])
        index.commit('Unittest Commit')

        PullPush.push(self.repos['test_pullpush_target'])

        was_pushed = os.path.exists(tmpfile.name)
        self.assertEqual(was_pushed, True)


if __name__ == "__main__":
    unittest.main()
    gd.proc.terminate()
