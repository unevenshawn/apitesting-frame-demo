import logging
import pytest
from api import yamlUtil

'''
scope的值可以为 ``"function"``(default), ``"class"``, ``"module"``, ``"package"`` or ``"session"``.

"session"级别用的比较多
'''


# 用于放置模块级别的fixtures，放在这儿的文件，属于该模块内的测试类能够访问到，模块外的类，无法访问到
@pytest.fixture(scope="session")
def startuplog():
    print("session test start")
    logging.info("session test start")


@pytest.fixture(scope="session", autouse=True)
def truncate_yml():
    f = open(file="extract.yml", mode="wb")
    if f is not None:
        f.truncate()


@pytest.fixture(scope="function", autouse=False)
def use_base_url(first_layer, second_layer):
    yamldata = yamlUtil.read_conf_yml()
    assert yamldata is not None
    url_1 = yamldata[first_layer]
    assert url_1 is not None
    url_2 = url_1[second_layer]
    return url_2
