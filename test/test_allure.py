import allure


@allure.epic("shawn接口自动化开发")
@allure.feature("简单测试allure模块命名")
class Test_Allure:
    @allure.story("allure测试的story级别")
    def test_pr(self):
        pass




@allure.epic("测试allure的测试类")
class Test_emptyClass:
    @allure.feature("应该是allure模块")
    def test_foo(self):
        pass