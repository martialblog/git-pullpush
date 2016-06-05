#!/usr/bin/env python3


import git
import tempfile
import time

tmpdir = tempfile.TemporaryDirectory(suffix='.git')
repo = git.Repo.init(tmpdir.name, shared=True, bare=True)

repo.daemon_export = True

gd = git.Git().daemon(tmpdir.name,
                      enable='receive-pack',
                      listen='127.0.0.1',
                      port=9418,
                      as_process=True,
                      verbose=True
)

time.sleep(0.5)

gd.proc.wait()

# filename = os.path.join(tmpdir.name, 'index.htm')
# with open(filename, "a") as f:
#     f.write("Hello World")
