def dict_traverse_replace(diction, begin_char, end_char, **keymap):
    for key, value in diction.items():
        if hasattr(value, 'keys'):
            dict_traverse_replace(value, begin_char, end_char, **keymap)
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
                diction[key] = replace_certain_keys(value, begin_char, end_char, **keymap)


# print(dict_traverse_replace({'a':'${expire}'}, "${", "}", **{"access": "jess", "expire": 2190}))

def replace_certain_keys(string, begin_char, end_char, **keymap):
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

# 去重
def removesesame(data):
    strls = list(str(data))
    templs = []
    for i in range(len(strls) - 1, -1, -1):
        if strls[i] not in templs:
            templs.append(strls[i])
    return ''.join(templs)


#将int转为string后切分
def slice_int_like_str(integer):
    string = list(str(integer))
    for i in range(len(string) - 1):
        if i == len(string) - 1:
            break
        for j in range(i + 1, len(string) - 1):
            if string[i] == string[j]:
                string.remove(string[j])
                i = i + 1
    return string