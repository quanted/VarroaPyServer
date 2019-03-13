import os, time


def clean_files(path, days=7):
    """
    This function cleans up files in a given folder that are older than a certain number of days
    :param path: the path to the folder to clean up
    :param days: remove files in the folder that are older than this
    :return: Nothing
    """
    now = time.time()
    cutoff = now - (days * 86400)
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            c_time = os.stat(file_path).st_ctime
            if c_time < cutoff and file != '.gitignore':
                os.remove(file_path)
