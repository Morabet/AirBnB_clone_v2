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
            archive_arr = archive_path.split('/')
            archive_full_name = archive_arr[1]
            archive_arr = archive_arr[1].split('.')
            archive_name = archive_arr[0]

            """Upload archive to the server"""
            put(archive_path, '/tmp')

            uncompress_fold = f"/data/web_static/releases/{archive_name}"
            tmp_location = f"/tmp/{archive_full_name}"

            """Run remote commands on the server"""
            run(f"mkdir -p {uncompress_fold}")
            run(f"tar -xvzf {tmp_location} -C {uncompress_fold}")
            run(f"rm {tmp_location}")
            run(f"mv {uncompress_fold}/web_static/* {uncompress_fold}")
            run(f"rm -rf {uncompress_fold}/web_static")
            run(f"rm -rf /data/web_static/current")
            run(f"ln -s {uncompress_fold} /data/web_static/current")
            run("sudo service nginx restart")
            return True
        else:
            return False
    except Exception:
        return False
