import re
import os


# print(__file__)  # __file__即為當前文件的绝对路径
# print(os.getcwd())

# 将pytest的各种插件，前面加上pytest-
def assemble_pytest_plugins(ls: list):
    newls = ["pytest"]
    for i in ls:
        if not filter_condition(i):
            pass
        else:
            newls.append("pytest-" + str(i))
    return newls


def assemble_all_as_list(d: dict):
    # 把'pytest'的值组装到列表中
    pls = list(assemble_pytest_plugins(d["pytest"]))

    # 将dict中key为common的值进行过滤
    ls = list(filter(lambda s: s and s.strip(), d['common']))

    print(ls, pls)
    ls.extend(pls)
    return ls


def filter_condition(origin):
    if origin == "" or type(origin) != str:
        return False
    return True


# 写入requirements文件
def write_requirements(d: dict):
    ls = assemble_all_as_list(d)
    with open(file=file, mode="w", encoding="utf-8") as f:
        for i in ls:
            f.writelines(i + "\n")


# 从文件中读取文件，并用对应的方式处理每一行文本
def excute_command_from_file(file, linehandler):
    with open(file=file, mode="r", encoding="utf-8")as f:
        for line in f:
            os.system(linehandler(line.strip()))


# 设计思想，handler，这儿是拼接入pip的完整命令，如果是其它命令，就用其它的handler
def piphandler(line: str):
    return f"pip install {line}"


# pip install -r requirements.txt
if __name__ == '__main__':
    file = "requirements.txt"
    data = {"pytest": {"xdist", "ordering", "rerunfailures", "base-url", "html"},
            "common": {"requests", "allure-pytest", "pyyaml", "openpyxl", "pymysql", "jsonpath", "flask", "rsa",
                       "redis","webdriver-helper"}}
    write_requirements(data)
    # print(install_requirements(f"pip install -r {file}"))
    excute_command_from_file(file=file, linehandler=piphandler)
    #  -i https://pypi.tuna.tsinghua.edu.cn/simple
    #  -i  http://mirrors.aliyun.com/pypi/simple/
