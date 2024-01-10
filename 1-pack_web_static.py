#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo"""

import datetime
from fabric.api import local


def do_pack():
    """Pack all the contents in the web_static directory
    as a tar archive"""

    try:
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_path = f"versions/web_static_{date}.tgz"
        local(f"tar -czvf {file_path} web_static")
        return file_path

    except Exection:
        return None
