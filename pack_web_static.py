from fabric.api import local
from datetime import datetime

def do_pack():
    # Generate a timestamp to include in the archive name
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    # Define the archive path, incorporating the timestamp
    archive_path = "versions/web_static_{}.tgz".format(date_time)

    # Create the 'versions' directory if it doesn't exist to store the archive
    local("mkdir -p versions")

    # Command to archive the 'web_static' directory, including all its contents
    # Explanation of the tar command options:
    # -c: Create a new archive
    # -v: Verbose mode, lists files processed (omitted here for script simplicity)
    # -z: Compress the archive with gzip, making it a .tgz file
    # -f: Specify the filename of the archive
    # The command effectively compresses the 'web_static' directory into a .tgz file
    archive_cmd = "tar -cvzf {} web_static".format(archive_path)

    # Execute the command and capture the result
    result = local(archive_cmd, capture=True)

    # Check if the command succeeded and return the archive path or None
    if result.failed:
        return None
    else:
        return archive_path

