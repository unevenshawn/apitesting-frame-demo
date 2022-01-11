import os
import re

import urllib3

from api.logUtil import error_log


def openFileReader(file):
    return open(file, mode="r", encoding="utf-8")


def closeFile(*files):
    for file in files:
        file.close()


def openFileWriter(file):
    return open(file, mode="w", encoding="utf-8")


def openBinaryFileReader(file):
    return open(file, mode="rb", encoding="utf-8")


def openBinaryFileWriter(file):
    return open(file, mode="wb", encoding="utf-8")


def join_path(filepath):
    return os.path.join(os.getcwd(), filepath)


def join(*paths):
    return os.path.join(*paths)


def get_path():
    return os.getcwd()

def url_join(*urls):
    """
    :param urls:只能使用基础路径的拼接，不支持param以键值对的形式进行拼接
    :return: 拼接完的url
    """
    try:
        first = urls[0]
        remaining = urls[1:]
        acceptls = []
        # 如果是协议名称，那么不管
        if re.match(r".*?://", first):
            pass
        else:
            if first[-1] == '/':
                # 如果末尾有/，那么去除掉
                first = first[0:-1]
        acceptls.append(first)
        for x in remaining:
            ele = x
            # 如果开头就是/，那么去掉
            if x[0] == "/":
                ele = x[1:]
            # 如果末位是"/"，那么删除掉
            if x[-1] == '/':
                ele = ele[0:-1]
            ele = "/" + ele
            # 把首尾的/都去掉了
            acceptls.append(ele)
        urls = "".join(acceptls)
    except Exception as e:
        error_log(e)
        raise Exception(e)
    return urls

if __name__ == '__main__':
    tt = [1, 2, 3, 4, 5]

    print(url_join(*(map(str,tt))))
