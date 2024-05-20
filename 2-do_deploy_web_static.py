#!/usr/bin/python3
""" This task is about deployment """
from fabric.api import *
from datetime import datetime
from os.path import exists
import os

env.hosts = ['54.236.53.167', '54.236.26.139']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/school'


@task
def do_pack():
    """ Fabric script that generates a .tgz archive from the contents of the
    web_static folder """
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
    """ Distribute archive to web servers """
    if not exists(archive_path):
        print(f"Error: Archive file {archive_path} not found")
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web servers
        put(archive_path, "/tmp/")
        archive_filename = os.path.basename(archive_path)
        archive_name_without_ext = os.path.splitext(archive_filename)[0]
        release_path = f'/data/web_static/releases/{archive_name_without_ext}'

        # Uncompress the archive to the /data/web_static/releases/ directory
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{archive_filename} -C {release_path}')
        
        # Move contents to the correct location
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')

        # Delete the archive from the web servers
        run(f'rm /tmp/{archive_filename}')

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run(f'ln -s {release_path} /data/web_static/current')

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
