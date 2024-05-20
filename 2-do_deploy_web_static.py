#!/usr/bin/python3
"""this task2 it's about deployment"""
from fabric.api import *
from datetime import datetime
from os.path import exists
import os


env.hosts = ['54.236.53.167', '54.236.26.139']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/school'

@task
def do_pack():
    # Implementation of do_pack function (from 1-pack_web_static.py)
    """ Fabric script that generates a .tgz archive from the contents of the...
    ...web_static folder """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None

@task
def do_deploy(archive_path):
    """for deploy"""
    # Step 1: Check if the specified archive file exists
    if not exists(archive_path):
        print(f"Error: Archive file {archive_path} not found")
        return False

    try:
        # Step 2: Upload the archive to the /tmp/ directory on the web servers
        put(archive_path, "/tmp/")

        # Step 3: Uncompress the archive to the /data/web_static/releases/ directory
        archive_filename = os.path.basename(archive_path)
        archive_name_without_ext = os.path.splitext(archive_filename)[0]
        release_path = f'/data/web_static/releases/{archive_name_without_ext}'
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{archive_filename} -C {release_path}')

        # Step 4: Delete the archive from the web servers
        run(f'rm /tmp/{archive_filename}')

        # Step 5: Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Step 6: Create a new symbolic link /data/web_static/current
        run(f'ln -s {release_path} /data/web_static/current')

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
