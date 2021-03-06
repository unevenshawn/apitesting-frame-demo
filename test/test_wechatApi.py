import json
import os
import random

import allure
import pytest
import requests

from api import requestUtil, yamlUtil, fileUtil, ddt
from api.requestUtil import RequestUtil
from test.hot_load_class import Inst


@allure.epic("shawn接口自动化开发")
@allure.feature("微信测试模块")
class Test_Wechat:
    session = RequestUtil(config_url_name="wechatApi", classinstance=Inst())
    tempTag = ''

    @allure.story("测试access_token获取")
    # 一个test方法，必须要对应一个yaml，因为不同的test_case，其数据请求是不相同的，后面的解析也不同，但是解析可以做到更好的robustness，将所有情况考虑在内，之后进行统一方法的调用
    # parametrize直接将yaml中的多条测试数据解析成一条一条的测试数据，不必再关注如何处理列表，只需关注列表中每一项的数据
    @pytest.mark.parametrize("casedata", ddt.read_testcase_yaml("test/test_get_token.yml"))
    # # 封装的终极结果，就是要让facade界面，只调用了一个简单的方法，所有的内在逻辑都放入背后的api中
    def test_token(self, casedata):
        self.session.standard_yaml(casedata)

    @allure.story("测试文件上传")
    @pytest.mark.parametrize("casedata", ddt.read_testcase_yaml("test/test_upload_file.yml"))
    def test_uploadFile_new(self, casedata):
        self.session.standard_yaml(casedata)

'''
如果是线性脚本代码就是如下内容所示，上方的用例，进行了代码和数据分离，分了 util， api testcase和data四个层级，通过yaml文件进行了数据驱动

# def test_uploadFile1(self):
#     method = "post"
#     #     # 文件上传关键点1，调用类名+字段名Test_Wechat，这样调用的是类的静态属性
#     #     # 猜测pytest框架在运行的时候，实际上实例化了多个测试类，所以导致如果绑定self.access_token，会导致无法绑定到同一个实例化对象上面。
#     url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=" + yamlUtil.read_yaml("extract.yml")[
#         'access_token']
#     #     # 文件上传关键点2，上传的文件要用open打开，并且要作为'media'的键值，作为数据提交
#     file = {"files": {'media': open(file=fileUtil.join_path("test/test.jpeg"), mode = "rb")}}
#     result = requests.session().request(method=method, url=url, **file)
#     print(result.text.replace(r"\/", '/'))
#
    
    
# def test_blackList(self):
#     url = "https://api.weixin.qq.com/cgi-bin/tags/members/getblacklist?access_token=" + yamlUtil.read_yaml("extract.yml")['access_token']
#     data = {
#         # "access_token": yamlUtil.read_yaml("extract.yml")['access_token'],
#         "begin_openid": ''
#     }
#     # 传入json数据的时候，要用json=xxx来传参
#     # 否则就要用json.dumps(data)
#     result = Test_Wechat.session.post(url=url, data=json.dumps(data))
#     print(result.text)
#
# def test_getTags(self):
#     url = "https://api.weixin.qq.com/cgi-bin/tags/get?access_token=" + yamlUtil.read_yaml("extract.yml")['access_token']
#     result = Test_Wechat.session.get(url=url)
#     print(result.text)
#
# def test_createTag(self):
#     url = "https://api.weixin.qq.com/cgi-bin/tags/create?access_token=" + yamlUtil.read_yaml("extract.yml")['access_token']
#     data = {"tag": {"name": "学习案例" + str(random.randint(1, 200))}}
#     result = Test_Wechat.session.post(url=url, json=data)
#     Test_Wechat.tempTag = json.loads(json.dumps(result.json()).replace(r"\\", "\\"))
#     print(Test_Wechat.tempTag)
#
# def test_editTag(self):
#     url = "https://api.weixin.qq.com/cgi-bin/tags/update?access_token=" + yamlUtil.read_yaml("extract.yml")['access_token']
#     data = Test_Wechat.tempTag
#     assert type(data) == dict
#     data['tag']['name'] = data['tag']['name'] + str(random.randint(200, 400))
#     result = Test_Wechat.session.post(url=url, json=data)
#     print(result.text)
#     print("修改成功") if result.json()['errcode'] == 0 else print("未修改成功")
#
# def test_dropTag(self):
#     url = "https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=" + yamlUtil.read_yaml("extract.yml")['access_token']
#     data = Test_Wechat.tempTag
#     assert type(data) == dict
#     assert data['tag']['name']
#     result = Test_Wechat.session.post(url=url, json=data)
#     print(result.text)
#     print("删除成功") if result.json()['errcode'] == 0 else print("未删除成功")
'''