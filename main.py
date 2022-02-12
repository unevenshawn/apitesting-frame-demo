# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import datetime
import json
import logging
import os
import queue
import re
import time

import openpyxl
import yaml
from jsonpath import jsonpath

from api import yamlUtil, fileUtil, logUtil, ddt, funcUtil, excelUtil, encryptUtil, redisUtil

j = {
    'name': 'wechat',

    'url': "${expire}",
    'method': 'get',
    'data': {'grant_type': 'client_credential',
             'appid': 'wx92dba2d5e2235bf6',
             'secret': '93ab60fda4d17acf364123${expire}'},

    'extract': {'access_token': '"access_token":(.*?)', 'expire_in': '$.expire_in'},
    'assertion': {
        'equals': [{'a': 'b'}, {'c': 'd'}],
        'contains': ['a', 'b', 'c']
    }
}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def a(file, data):
    with open(file=file, mode="a+") as f:
        yaml.dump(data=data, stream=f)


def t(data):
    string = str(data)
    string = list(string)
    ls = []

    # for i in range(len(string)-1):
    #     temp=string[i]
    temlen = len(string) - 1
    removed = 0
    for i in range(len(string) - 1, -1, -1):
        if i < 1:
            break
        for j in range(i - 1, -1, -1):
            if string[i] == string[j]:
                string.remove(string[j])
                i = i - 1
    while len(string) != 0:
        ls.append(string.pop())
    print(ls)
    return "".join(ls)


def removesesame(data):
    strls = list(str(data))
    templs = []
    for i in range(len(strls) - 1, -1, -1):
        if strls[i] not in templs:
            templs.append(strls[i])
    return ''.join(templs)


def get_index(string, target, start_index):
    return string.index(target, start_index)


# def replace_certain_keys(diction, begin_char, end_char, **keymap):
#
#     string = json.dumps(diction)
#     typedict = {}
#     for i in range(1, string.count(begin_char) + 1):
#         if begin_char in string and end_char in string:
#             start_index = string.index(begin_char)
#             end_index = string.index(end_char, start_index)
#             old_value = string[start_index:end_index + len(end_char)]
#             key_for_keymap = old_value[len(begin_char):len(old_value) - len(end_char)]
#             new_value = keymap[key_for_keymap]
#             # 判断Key对应的类型，如果不是整数，那么转换成string
#
#             if type(new_value) is int or type(new_value) is float:
#                 typedict[key_for_keymap] = type(new_value)
#                 new_value = str(new_value)
#             string = string.replace(old_value, new_value)
#
#     # 暂时不支持所存储的局部变量进行加减乘除等运算，如果要支持，需要加一个正则表达式进行匹配
#     # 如果只出现一次，将key对应的值再转换回去其类型
#     resultjson = json.loads(string)
#
#     if len(typedict.keys()) > 0:
#         for key in typedict.keys():
#             replace_valuetype_by_key(key, typedict, resultjson)
#     return resultjson

'''
思路
区别对待，看是str，list或者是dict
遍历dict，对每一个key:value，找出value的type为str的
value的中从${a}到实际值的对应，应该来自于yaml文件
'''


def list_in_yaml():
    data = yamlUtil.read_yaml("test.yml")
    yamlUtil.write_yaml("test1.yml", data)


def ioi():
    jso = yamlUtil.read_yaml("test.yml")
    jso_string = json.dumps(jso)
    temp_caseinfo = jso_string
    data_list = "abc"
    data_list2 = 1234
    temp_caseinfo = temp_caseinfo.replace('"${' + data_list + '}"', str(data_list2))
    return json.loads(temp_caseinfo)


solid = [
    {
        'name': '删除创建的标签',
        'parameterize': {'name-tag_id': '/datas/product_manage/delete_flag_data.yaml'},
        'request': {
            'method': 'post',
            'url': '/cgi-bin/tags/delete?access_token=${read_extract_data(access_token)}',
            'json': {
                'tag': {'id': '${read_extract_data(tag_id)}'}
            }
        },
        'validate': [{'equals': {'status_code': 200}}]
    },
    {
        'name': '删除系统标签', 'parameterize': {'name-tag_id': '/datas/product_manage/delete_flag_data.yaml'},
        'request': {
            'method': 'post', 'url': '/cgi-bin/tags/delete?access_token=${read_extract_data(access_token)}',
            'json': {'tag': {'id': 1}}
        },
        'validate': [{'equals': {'status_code': 200}}]
    }
]

solod = solid[0]


def enco_deco():
    a = "就这样吧aabcdsedf"
    u = bytes(a, "unicode_escape")

    u1 = u.decode("unicode_escape")

    # u=u.decode("utf-8")
    print(u, "\n", u1)
    # print(bb)


class dt:
    str1 = {"a": "$ddt(name)", "b": "$ddt(pass)", "c": "$ddt(user)", "d": "$ddt(mail)"}
    str2 = ["$ddt(pass)", "$ddt(mail)", "$ddt(name)", "$ddt(user)"]
    ls = [
        ["name", "pass", "user", "mail"],
        ["ali", "123", "admin", "admin@ali.com"],
        ["bob", "987", "common", "common@bob.com"],
    ]


def mt(string: str, ls: list):
    string1 = json.dumps(string)
    new_ls = []
    for i in range(1, len(dt.ls)):
        temp_string1: str = string1
        for j in range(len(ls[i])):
            try:
                value = int(ls[i][j])
                temp_string1 = temp_string1.replace('"$ddt(' + ls[0][j] + ')"', str(value))
            except Exception as e:
                print(e)
            else:
                print(ls[i][j])
                temp_string1 = temp_string1.replace('$ddt(' + ls[0][j] + ')', ls[i][j])
        new_ls.append(json.loads(temp_string1))
    return new_ls


def ty():
    a = "http://mmbiz.qpic.cn/"
    b = "http:\/\/mmbiz.qpic.cn\/"
    # c = b.encode("utf-8").decode("unicode_escape")
    print("\/" in b)
    print(b.replace("\/", "/") == a)


def ttt():
    a = 'http://mmbiz.qpic.cn/mmbiz_jpg/46DYv1xP20R7qPBq2yO5u9ZyFyzkvuvhVzlqHbVQ3J3oibOTwwOBl7IdiaZwqyjtdGqOAcT6nQJXt0WzOtLqAHcA/0'
    b = not None
    print(a is b)
    print(not None == yamlUtil.read_conf_yml("url"))


class T:
    tattr = 'joseph'

    def gettattr(self):
        return self.tattr


def gt() -> logging.Logger:
    gt_logger = logging.getLogger()
    hdler = logging.FileHandler(str(time.time()) + ".log", encoding="utf-8")
    gt_logger.setLevel(logging.DEBUG)
    gt_logger.addHandler(hdler)
    return gt_logger


def b64():
    uu = str(dt.str2)
    print(uu)
    bsf = base64.b64encode(uu.encode("utf-8"))
    bsft = base64.b64decode(bsf)
    print(bsf, bsft)


def dictkeys():
    print(list(solid[0].keys())[0])


def split_or_replace():
    string = "url-grant_type-appid-secret-equals"
    replaced = "-"
    to_replace = ","
    print(string.replace(replaced, to_replace))


def test_queue():
    ls = queue.Queue()

    ls.put(1)
    ls.put(2)
    print(ls.get(), ls.get())


def list_in_dict(key, value, traverse):
    t_type = type(value)
    if t_type == list or t_type == tuple:
        print(key, value)
        for l in value:
            if type(l) == dict:
                traverse(l)
    elif None:
        pass
    ls = []


def dict_print(key, *value):
    temp_value = None

    if len(value) < 1:
        temp_value = key
        temp_type = type(temp_value)
        if temp_type == dict or temp_type == list:
            return
        if temp_type == str:
            print(f"数组元素的值为字符串类型：{key}")
        if temp_type == int or temp_type == float:
            print(f"数组元素的值为数值类型：{key}")
    else:
        temp_value = value[0]
        temp_type = type(temp_value)
        if temp_type == dict or temp_type == list:
            return
        if temp_type == str:
            print(f"dict的值为字符串类型：{key}, {temp_value}")
        if temp_type == int or temp_type == float:
            print(f"dict的值为数值类型：{key}, {temp_value}")


def b64():
    ss = "hh".encode()
    b_dc = base64.b64encode(ss).decode("utf-8")
    print(b_dc)
    bst = b_dc.encode('utf-8')
    ac = base64.b64decode(bst)
    print(ac)

def redis_try():
    con = redisUtil.connect()
    print(con)
    con.set("api_test_in_python", "to strive for better salary and life")
    st:bytes=con.get("api_test_in_python")
    print(st.decode("utf-8"))
    con.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # oldvalue = "${abc}"
    # print(json.dumps({"test": "${abc}"}).replace('"' + "${abc}" + '"', str(1234)))
    # print(type("${abc}".replace("${abc}", str(1234))))
    # print("abcdefghjkl${weq}".replace('""'))
    # print(ioi())
    # print(mt(dt.str1,dt.ls))
    # ty()
    # print(str(int(time.time())))
    # logUtil.error_log("an error occurred")
    # logUtil.info_log("info to inform of you")
    # print(dt())
    # split_or_replace()
    # print(funcUtil.compare_if_same(['name', 'grant_type', 'appid', 'secret', 'equals'], ['name', 'grant_type', 'appid', 'secret', 'contains']))
    # print(fUtil.compare_if_same([1, 2, 3], [1, 2, 3]))
    # print(json.loads(funcUtil.replace_json_str_if_int(json.dumps(solid),"read_extract_data(tag_id)",111)))
    # print(json.loads(funcUtil.replace_json_str_if_int(json.dumps(solid),"read_extract_data(access_token)",111)))
    # print("'"=='"')
    # funcUtil.dict_traverse(j, dict_print)
    # ddt.read_testcase_yaml("test/test_get_token.yml")
    # encryptUtil.gen_key("data")
    # confid=encryptUtil.pbk_encrypt("data/public.pem","use my power")
    # ct=encryptUtil.prk_decrypt("data/private.pem",confid)
    # print(encryptUtil.b64encrypt("23"))
    # print(encryptUtil.b64decode(encryptUtil.b64encode("utf")))
    # redis_try()

    pass
