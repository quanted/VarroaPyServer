import os, time


def clean_files(path, days=7):
    now = time.time()
    cutoff = now - (days * 86400)
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            print(file)
            c_time = os.stat(file_path).st_ctime
            if c_time < cutoff and file != '.gitignore':
                os.remove(file_path)
