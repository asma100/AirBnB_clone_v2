#!/usr/bin/python3
""" generates a .tgz archive"""



from fabric.api import *
from datetime import datetime


def do_pack():
    """  ates a .tgz a"""
    local("sudo mkdir -p versions")
    t = datetime.now().strftime("%Y%m%d%H%M%S")
    name = "versions/web_static_{}.tgz".format(t)
    result = local("sudo tar -cvzf {} web_static".format(name))
    if result.succeeded:
        return name
    else:
        return None
