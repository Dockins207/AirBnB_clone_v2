#!/usr/bin/python3
# Fabfile to create and distribute an archive to web servers.
from fabric import Connection, task
from datetime import datetime
import os

# Define your hosts
hosts = ["100.25.167.199", "54.210.59.141"]

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    if not os.path.isdir("versions"):
        os.makedirs("versions")
    local_cmd = "tar -cvzf {} web_static".format(file_name)
    result = local(local_cmd, capture=True)
    if result.failed:
        return None
    return file_name

def do_deploy(archive_path, host):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
        host (str): The host to deploy to.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]

        # Start a new connection to the given host
        c = Connection(host)
        c.put(archive_path, "/tmp/{}".format(file))
        c.run("rm -rf /data/web_static/releases/{}/".format(name))
        c.run("mkdir -p /data/web_static/releases/{}/".format(name))
        c.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
        c.run("rm /tmp/{}".format(file))
        c.run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        c.run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        c.run("rm -rf /data/web_static/current")
        c.run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

def deploy():
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    results = []
    for host in hosts:
        result = do_deploy(archive_path, host)
        results.append(result)
    return all(results)

# Helper function to execute local commands, needed for do_pack
def local(cmd, capture=False):
    """Function to mimic Fabric 1's local command execution"""
    import subprocess
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        if capture:
            return output.decode('utf-8')
        else:
            print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(e.output.decode('utf-8'))
        return None

