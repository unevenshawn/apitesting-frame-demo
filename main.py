# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import yaml
from jsonpath import jsonpath

from api import yamlUtil

j={
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


def t1(integer):
    string = list(str(integer))
    for i in range(len(string) - 1):
        if i == len(string) - 1:
            break
        for j in range(i + 1, len(string) - 1):
            if string[i] == string[j]:
                string.remove(string[j])
                i = i + 1
    return string


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
def dict_traverse_replace(diction,begin_char,end_char,**keymap):

    for key, value in diction.items():
        if hasattr(value, 'keys'):
            dict_traverse_replace(value,begin_char,end_char, **keymap )
            """
            #待解决，如果是list，该怎么迭代
        elif isinstance(value,list):
            for element in value:
                if isinstance(element,dict):
                    dict_traverse_replace(element,begin_char,end_char,**keymap)
            """
        else:
            # 后续需要考虑，如果value为数组，那么要怎么办
            if type(value) == str:
                diction[key]=replace_certain_keys(value,begin_char,end_char,**keymap)

# print(dict_traverse_replace({'a':'${expire}'}, "${", "}", **{"access": "jess", "expire": 2190}))

def replace_certain_keys(string, begin_char, end_char, **keymap):
    if string.count(begin_char)==0:
        return string
    temp_type=None
    new_string = ""
    flag2int=string.count(begin_char)==1 and string.index(begin_char)==0
    """
    在这儿需要增加针对多个`${}`的加减乘除运算，这儿只考虑了{"a":${intvalue}}这一种值为int的情况
    """

    for i in range(1, string.count(begin_char) + 1):
        if begin_char in string and end_char in string:
            start_index = string.index(begin_char)
            end_index = string.index(end_char, start_index)
            old_value = string[start_index:end_index + len(end_char)]
            key_for_keymap = old_value[len(begin_char):len(old_value) - len(end_char)]
            new_value = keymap[key_for_keymap]
            # 判断Key对应的类型，如果不是整数，那么转换成string

            if type(new_value) is int or type(new_value) is float:
                temp_type = type(new_value)
                new_value = str(new_value)
            new_string = string.replace(old_value, new_value)
            string = new_string
    # 暂时不支持所存储的局部变量进行加减乘除等运算，如果要支持，需要加一个正则表达式进行匹配
    # 如果只出现一次，将key对应的值再转换回去其类型
    if flag2int and (temp_type is int or temp_type is float):
        new_string = temp_type(string)
    return new_string



def read_yaml_by_key(key):
    data = yamlUtil.read_yaml(r"C:\Users\Uneven\Desktop\codes\python\api_test\test\wechat.yml")
    return data[key]


def tt():
    j = [
        {
            'name': 'wechat',
            'request':
                {
                    'url': 'https://api.weixin.qq.com/cgi-bin/token',
                    'method': 'get',
                    'data': {'grant_type': 'client_credential',
                             'appid': 'wx92dba2d5e2235bf6',
                             'secret': '93ab60fda4d17acf3641232de67f6dd3'}
                },
            'extract': {'access_token': '"access_token":(.*?)', 'expire_in': '$.expire_in'},
            'assertion': {
                'equals': [{'a': 'b'}, {'c': 'd'}],
                'contains': ['a', 'b', 'c']
            }
        }
    ]

    print(jsonpath.jsonpath(j, "$..appid"))


def aa():
    ls = ["a0"]
    a = ls[0]
    b = "a0"
    print(a == b)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print("${access}".replace("${access}", "jess"))
    # print(replace_certain_keys("a===${access}${expire}", "${", "}", **{"access": "jess", "expire": 2190}))
    # a={'a':'${expire}'}
    # print(dict_traverse_replace(j, "${", "}", **{"access": "jess", "expire": 2190}))
    # print(j)
    # print(type(replace_certain_keys("${expire}", "${", "}", **{"access": "jess", "expire": 2190})))
    # print(type(123) is int)

    print()