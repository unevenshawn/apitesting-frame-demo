import json

import requests

from api import yamlUtil, fileUtil
from api.yamlUtil import read_yaml


class RequestUtil:
    # session默认会自动关联cookie
    __session = requests.session()
    project_base_url = ''

    def __init__(self, config_url):
        self.project_base_url = config_url

    def send_request(self, url, method, **kwargs):
        full_url = fileUtil.join_path(yamlUtil.read_conf_yml(self.project_base_url), url)
        pass

    def standard_yaml(self, yamldata):
        """
        yaml中数据读取出来后，得到的即是如下的数据内容
        ls = [
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
        """
        self.has_necessary_keys(['name', 'request', 'assertion'], **yamldata)
        self.replace_extract_yaml(diction=yamldata,**read_yaml("extract.yml"))

    def replace_extract_yaml(self, diction, **extractyaml):
        self.dict_traverse_replace(diction,'${','}',replace_method_for_hotload_func,**extractyaml)

    def replace_extract_and_hotload_func(self, diction,classinstance, **extractyaml):
        self.dict_traverse_replace(diction, '#{', '}', replace_method_for_hotload_func,classinstance=classinstance, **extractyaml)

    '''
    运用思路
    区别对待，看是str，list或者是dict
    遍历dict，对每一个key:value，找出value的type为str的
    value的中从${a}到实际值的对应，应该来自于yaml文件
    
    另外来说，replace_for_one_func实际上是要传入一个函数名称进行，是一个替换方法
    
    '''

    def dict_traverse_replace(self, diction, begin_char, end_char, replace_for_one_func,classinstance=None, **keymap):

        for key, value in diction.items():
            if hasattr(value, 'keys'):
                self.dict_traverse_replace(value, begin_char, end_char, replace_for_one_func, **keymap)
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
                    # 传入的替换方法，类似于java的各种handler
                    diction[key] = replace_for_one_func(value, begin_char, end_char,classinstance=classinstance, **keymap)

    # print(dict_traverse_replace({'a':'${expire}'}, "${", "}", **{"access": "jess", "expire": 2190}))

    def has_necessary_keys(self, *keys, **kwargs):
        dictkeys = kwargs.keys()
        for key in keys:
            if key not in dictkeys:
                print("未包含必须的键")

    @property
    def session(self):
        return self.__session

    def __request(self, method, url, *params, **data):
        return self.session.request(method, url, *params, **data)

    # get请求方式，传参只有param
    def __get(self, url, param):
        return self.session.request(url, params=param)

    def __getCookie(self):
        return self.session.cookies

    def __post(self, url, data, json):
        return self.session.request(url, data=data)

"""
可以供自定义选择符号进行匹配，比如这儿用的是#{}，还可以考虑@{},:{}等等, 
begin_char即是#{，end_char即为}
classinstance是热加载函数的实例化类对象，
extract_yaml就是从extract.yml读取数据

但还有个缺点，无法进行嵌套函数#{a(bz())}这种的替换和调用
"""
def replace_method_for_hotload_func( string, begin_char, end_char, classinstance, **extract_yaml):
    if string.count(begin_char) == 0:
        return string
    flag2int = string.count(begin_char) == 1 and string.index(begin_char) == 0
    temp_type = None
    islist = False
    for i in range(1, string.count(begin_char) + 1):
        if begin_char in string and end_char in string:
            # 例如用#{}来获取函数名
            #   #{的起始index
            start_index = string.index(begin_char)
            #   }的结束index
            end_index = string.index(end_char, start_index)
            # 如果${key}出现在首位，后续没有字符串，才会将flage2int继续置为True，否则为False
            if string.count(begin_char) == 1:
                flag2int = (end_index + 1 - start_index) == len(string)
            #  #{func()}
            old_value = string[start_index:end_index + len(end_char)]
            #  #{func()}->func()
            instance_method_name = old_value[len(begin_char):len(old_value) - len(end_char)]
            func_bracket_start_index = instance_method_name.index("(")
            func_bracket_end_index = instance_method_name.index(")")
            args = instance_method_name[func_bracket_start_index + 1:func_bracket_end_index].split(",")
            # 如果#{func(arg1,arg2,arg3)}中有的是extract中的变量，那么进行替换
            for index in range(len(args)):
                if args[index] in extract_yaml.keys():
                    args[index] = extract_yaml[args[index]]
            func_name = instance_method_name[0:func_bracket_start_index]
            func_result = None
            if classinstance == None:
                print("传入热加载函数实例为空，或实例不存在")
            if len(args) > 1:
                func_result = getattr(classinstance, func_name)(*args)
            else:
                func_result = getattr(classinstance, func_name)()
            # 如果func的结果是int或float
            if type(func_result) is int or type(func_result) is float :
                flag2int = flag2int and isinstance(func_result, [int, float])
                temp_type = type(func_result)
                func_result = str(func_result)
            # 因为对dict进行了深度遍历，只获取值来进行替换，所以不可能是dict
            elif type(func_result) is  dict or type(func_result) is list:
                islist = True
                func_result = json.dumps(func_result)
                flag2int=False
            else:
                flag2int=False
            string = string.replace(old_value, func_result)
        if flag2int:
            string = temp_type(string)
        elif islist:
            string = json.loads(string)
        return string


def replace_certain_keys(string, begin_char, end_char, **keymap):
    # 如果不包含特殊符号，就将原数据返回
    if string.count(begin_char) == 0:
        return string
    temp_type = None
    new_string = ""
    flag2int = string.count(begin_char) == 1 and string.index(begin_char) == 0
    """
    在这儿需要增加针对多个`${}`的加减乘除运算，这儿只考虑了{"a":${intvalue}}这一种值为int的情况
    """
    for i in range(1, string.count(begin_char) + 1):
        if begin_char in string and end_char in string:
            start_index = string.index(begin_char)
            end_index = string.index(end_char, start_index)
            # 如果${key}出现在首位，后续没有字符串，才会将flage2int继续置为True，否则为False
            if string.count(begin_char) == 1:
                flag2int = (end_index + 1 - start_index) == len(string)
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


if __name__ == '__main__':
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
        },
        'al':'#{it()}'
    }

    class gg:
        def it(self):
            return "it"

    a = {'a': '${expire}'}
    r = RequestUtil("a")
    r.dict_traverse_replace(j, "${", "}", replace_certain_keys, **{"access": "jess", "expire": 2190})
    print(j)
    r.dict_traverse_replace(j,"#{","}",replace_method_for_hotload_func,classinstance=gg())
    print(j)
