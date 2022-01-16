import json

from api import yamlUtil, fileUtil, funcUtil
from api.logUtil import error_log, info_log


def read_testcase_yaml(filepath):
    yamldata = yamlUtil.read_yaml(filepath)
    jsonstring = json.dumps(yamldata)
    rtn_data = None
    if "parameterized" in jsonstring:
        rtn_data = process_parameterize(yamldata)
    else:
        rtn_data = yamldata
    return rtn_data


def process_parameterize(casedata):
    temp_casedata = None
    # 增加代码健壮度，防止以“-”开头
    if type(casedata) == list:
        temp_casedata = casedata[0]
    else:
        temp_casedata = casedata
    parameterized_dict: dict = temp_casedata["parameterized"]
    """
    考虑parameterized下面仅有一组数据
    考虑了parameterized下面有多组数据，存在多组数据时，实际的组装逻辑是差不多的
    但其实不会存在多组数据
    """

    # 读取原yaml parameterized下的key和value
    ddt_keys = list(parameterized_dict.keys())[0]
    path = parameterized_dict[ddt_keys]

    # 将parameterized对应的目录与项目根目录拼接，并读取对应yaml数据
    ddt_yml = yamlUtil.read_yaml(fileUtil.join(yamlUtil.get_path(), path))

    # ddt的yaml中，第一组数据必定是keys，将该组数据与原yaml的parameterized下的各关键字进行比对,检查核对是否一致
    # print(funcUtil.compare_if_same(ddt_keys.split("-"), ddt_yml[0]))
    if not funcUtil.compare_if_same(ddt_keys.split("-"), ddt_yml[0]):
        error_log("数据驱动yaml中的关键字与原测试用例的yaml文件中关键字不匹配")

    # 将原有的yaml文件内容转换成string，方便后续${ddt(name)}的替换
    yaml_string = json.dumps(temp_casedata)

    # 通过数组存放后续组装的
    assembled = []

    # 得到的是一个二维列表，第一组数据即是做数据驱动的keys，所以跳过第一组数据
    for i in range(1, len(ddt_yml)):
        # 从这儿开始，抽取第一条数据进行组装；
        # 因为一个原yaml文件对应多条ddt的数据，所以需要在每行开始前，抽取原yaml内容作为模板，之后在每一列中进行数据替换
        new_string = yaml_string
        for j in range(len(ddt_yml[i])):
            # 对每一列的数据，找到它第一组的对应列key，之后在原yaml转化的string中进行替换

            ddt_key = ddt_yml[0][j]
            ddt_value=ddt_yml[i][j]
            # 用实际的对应值来替换${ddt(key)},${和}在funcUtil中已经写死了，所以只要组装上ddt(key)就行
            new_string=funcUtil.replace_json_str_if_int(new_string,"ddt("+ddt_key+")",ddt_value)
            json_dict=json.loads(new_string)
        assembled.append(json_dict)
    info_log(f"数据驱动组装的数据为:{assembled}")
    return assembled