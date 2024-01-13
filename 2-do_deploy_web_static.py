#!/usr/bin/python3
""""Fabric script that distributes an archive to web servers"""

from fabric.api import *
import os

env.hosts = ['34.207.63.157', '54.85.3.206']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Archive distributor"""
    try:
        if os.path.exists(archive_path):
            full_name = archive_path.split('/')[1]
            location = file_name.split('.')[0]
            path_location = f"/data/web_static/releases/{location}"

            """Upload archive to the server"""
            put(archive_path, '/tmp/')
            """Run remote commands on the server"""
            run(f"mkdir -p {path_location}")
            run(f"tar -xzf /tmp/{full_name} -C {path_location}")
            run(f"rm /tmp/{full_name}")
            run(f"mv {path_location}/web_static/* {path_location}")
            run(f"rm -rf {path_location}/web_static")
            run(f"rm -rf /data/web_static/current")
            run(f"ln -s {path_location} /data/web_static/current")
            return True
        else:
            return False
    except Exception:
        return False
