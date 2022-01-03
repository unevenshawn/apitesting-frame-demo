import os


def openFileReader(file):
    return open(file, mode="r", encoding="utf-8")


def closeFile(*files):
    for file in files:
        file.close()


def openFileWriter(file):
    return open(file, mode="w", encoding="utf-8")

def openBinaryFileReader(file):
    return open(file,mode="rb",encoding="utf-8")

def openBinaryFileWriter(file):
    return open(file, mode="wb", encoding="utf-8")

def join_path(filepath):
    return os.path.join(os.getcwd(),filepath)