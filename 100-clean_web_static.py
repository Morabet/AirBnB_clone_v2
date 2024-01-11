#!/usr/bin/python3
# Fabscrip that deletes out-of-date archives.

import os
from fabric.api import *

env.hosts = ['34.207.63.157', '54.85.3.206']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Delete out-of-date archives """

    number = 1 if int(number) == 0 else int(number)

    list_file = sorted(os.listdir("versions"))
    for i in range(number):
        list_file.pop()
    with lcd("versions"):
        for y in list_file:
            local(f"rm ./{y}")

    with cd("/data/web_static/releases"):
        list_file = run("ls -tr").split()
        lis_file = [a for a in list_file if "web_static_" in a]
        for i in range(number):
            list_file.pop()
        for y in list_file:
            run(f"rm -rf ./{y}")
