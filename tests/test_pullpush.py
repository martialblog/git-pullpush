#!/usr/bin/env python3


import pytest
import tempfile
import time
import git
import os
import shutil
import pullpush.pullpush as pp


EXIT_0 = 0 << 8
EXIT_1 = 1 << 8
EXIT_2 = 2 << 8

TMP_DIR = tempfile.mkdtemp(suffix='pullpush-unittest-repos')
PORT = 4567


@pytest.fixture(scope="session")
def repositories(request):

    repos = {
        'test_pullpush_origin': 'URL',
        'test_pullpush_target': 'URL',
    }

    for reponame in repos.keys():
        repo_dir = os.path.join(TMP_DIR, reponame)
        repo = git.Repo.init(repo_dir, shared=True, bare=True)
        repo.daemon_export = True
        repos[reponame] = "git://localhost:%s%s%s" % (PORT,
                                                      TMP_DIR,
                                                      '/'+reponame)

    def fin():
        shutil.rmtree(TMP_DIR)
    request.addfinalizer(fin)

    return repos


@pytest.fixture(scope="session")
def gitdaemon(request):

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


    def fin():
        gd.proc.terminate()
    request.addfinalizer(fin)

    return gd


def test_pull(repositories, gitdaemon):
    """
    We test if an empty directory has a .git directory after the pull.
    """

    repo_dir = os.path.join(TMP_DIR, 'test_pull_repo')
    PullPush = pp.PullPush(repo_dir=repo_dir)

    PullPush.pull(repositories['test_pullpush_origin'])

    was_pulled = os.path.isdir(repo_dir + '/.git')
    assert(was_pulled == True)


def test_set_remote_url(repositories, gitdaemon):
    """
    We pull a repo, change the remote url and see if it got changed.
    """

    expected_url = 'unittest_url'
    repo_dir = os.path.join(TMP_DIR, 'test_remoteurl_repo')
    PullPush = pp.PullPush(repo_dir=repo_dir)

    PullPush.pull(repositories['test_pullpush_origin'])
    PullPush.set_remote_url(expected_url)

    origin = PullPush.repo.remotes.origin
    cr = origin.config_reader
    actual_url = cr.get_value('url')

    assert(actual_url == expected_url)


def test_push(repositories, gitdaemon):
    """
    We push a file to a target repo and see if it's there.
    """

    repo_dir = os.path.join(TMP_DIR, 'test_push_repo')
    PullPush = pp.PullPush(repo_dir=repo_dir)

    PullPush.pull(repositories['test_pullpush_origin'])

    tmpfile = tempfile.NamedTemporaryFile(dir=repo_dir)
    index = PullPush.repo.index
    index.add([tmpfile.name])
    index.commit('Unittest Commit')

    PullPush.push(repositories['test_pullpush_target'])

    was_pushed = os.path.exists(tmpfile.name)
    assert(was_pushed == True)

def test_main_success(repositories, gitdaemon):

    _from = repositories['test_pullpush_origin']
    _into = repositories['test_pullpush_target']

    command = '/usr/bin/env python3 pullpush/main.py --from ' + _from + ' --into ' + _into + ' > /dev/null'
    print(command)
    status = os.system(command)

    assert(status == EXIT_0)

def test_main_success_with_notify(repositories, gitdaemon):

    _from = repositories['test_pullpush_origin']
    _into = repositories['test_pullpush_target']

    command = '/usr/bin/env python3 pullpush/main.py --notify --from ' + _from + ' --into ' + _into + ' > /dev/null'
    print(command)
    status = os.system(command)

    assert(status == EXIT_0)
