#!/usr/bin/python3
# Fabfile to distribute an archive to web servers.
from fabric import task
import os

hosts = ["100.25.167.199", "54.210.59.141"]

@task(hosts=hosts)
def do_deploy(c, archive_path):
    """Distributes an archive to a web server.
    """
    if not os.path.isfile(archive_path):
        print("File not found: {}".format(archive_path))
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    try:
        # Assuming operations similar to the ones you specified
        c.run("echo 'Performing operations on the server'")
        # Add your deployment logic here
        return True
    except Exception as e:
        print(e)
        return False

