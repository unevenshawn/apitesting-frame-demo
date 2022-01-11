import os

import yaml


# 读模式
# r
# 打开不存在的文件会报错、不能写；如不指定模式则默认是r
# 写模式
# w
# 打开不存在的文件会, 会新建一个文件；打开存在的文件会先清空后覆盖原有文件；不能读
# 追加模式
# a
# 打开不存在的文件会, 会新建一个文件；不能读
#
# 读写模式
# r + 能写，打开不存在的文件会报错
# 写读模式
# w + 能读，但是读不到内容，因为w先把文件内容清空了
# 追加读模式
# a + 能读，但读不到内容，因为文件指针默认在最后一行，可用seek移动文件指针位置

# 直接填写相对路径，而不用管项目路径
def read_yaml(filename):
    with open(file=os.path.join(get_path(), filename), mode="r", encoding="utf-8") as f:
        yamldata = yaml.load(f, Loader=yaml.FullLoader)
        return yamldata


def read_yaml_bykeys(filename, *keys):
    data = read_yaml(filename)
    if (len(keys) == 1):
        data = data[keys[0]]
    else:
        for key in keys:
            data = data[key]
        # print(f"key is {i}")
    return data


def write_yaml(filename, data):
    with open(file=os.path.join(get_path(), filename), mode="w", encoding="utf-8") as f:
        yaml.dump(data=data, stream=f)


def write_to_extract_yml(data):
    with open(file=os.path.join(get_path(), "extract.yml"), mode="a+") as f:
        yaml.dump(data=data, stream=f)


def read_conf_yml(*keys):
    data = read_yaml_bykeys("config.yml", *keys)
    return data


def read_config_yaml_by_keys(*keys):
    data = read_yaml_bykeys("config.yml", *keys)
    return data


def read_extract_yaml_by_keys(*keys):
    data = read_yaml_bykeys("extract.yml", *keys)
    return data


def get_path():
    return os.getcwd()


def not_project_read(filename):
    with open(file=filename, mode="r", encoding="utf-8") as f:
        yamldata = yaml.load(f, Loader=yaml.FullLoader)
        return yamldata


if __name__ == '__main__':
    print(
        get_path()
    )
