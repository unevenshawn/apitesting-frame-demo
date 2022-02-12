# 自动化测试
## 接口自动化

### 使用说明
1. 在已经安装了python的环境下，先运行install_pip_script.py来安装必备的python插件，
2. 如果要连接数据库、redis等，在项目根目录下配置confid.yml，用于存放和读取数据库用户名和密码，该文件已被添加在gitignore中，只会保存在本地
3. 如果要运行脚本，run.py是入口
4. 运行前要从`http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login` 获取你的`appid`和`secret`，并作为用例配置到testdrive.yaml中
5. 运行结果应该是4成功，3失败，3个失败的是testdrive.yaml中的反例

### 要点总结
#### 前置内容

1. 对`python`语言熟悉，知道用`python`如何进行编码
2. 了解`pytest`的应用
3. 对测试的对象和系统有所理解
4. 掌握测试用例的编写

#### 已经完成的内容

1. 安装接口自动化测试所需要的各个组件和为`pytest`配套开发的插件

2. `pytest`的应用，使用`pytest`框架获取各个test类，通过`pytest.main`方法去运行各个测试用例，用方法`pytest.fixture`搭建起脚手架，通过`pytest.ini`获取基础配置信息

3. 对`requests`对象进行统一的封装，给一个统一的请求入口

4. 对`yaml`读取，进行封装，提供各类方法，比如返回`yaml`读取的总结果，比如根据`key`从`yaml`中得到`key`的值

5. 模块化，对于各个模块进行分离，

   - `testcase`为一个模块，工具等`api`单独放一个模块，用例加载和工具封装分离，降低耦合，同时也可以减少代码的重复

   - 由于每一个测试用例执行时，其数据结构都不大相同，每一个`testcase`的用例，对应一个`yaml`（也就是说，实际上框架搭建起来后，要做的主要事情就是针对测试用例设计`yaml`格式，并编写`yaml`解析规则）

   - 模块级别的`pytest.fixture`应用，则体现或者说放置于`conftest.py`文件中

     

#### 接下来要完成的内容（已完成）

1. 完善`requestUtil`和`yamlUtil`的封装

2. 对每一个`testcase`进行`yaml`参数化的读取

3. 对`yaml`文件书写进行规范，让框架使用者能够按照统一的格式输入测试数据，让测试用例的输入能够被获取识别到，进行一级目录`name`, `request`, `param/data`的解析

4. 根据正则表达式，或者`jsonpath`对全局变量进行匹配后提取，写入临时存储的`yaml`文件，并在会话中提取使用

5. 对`${}`的解析，能够将想要提取的变量以`key:value`的形式写入到`yaml`文件中，并能够在多个地方，（包含`request`,`url`,`headers`,`data`中能够提取得到）

6. 热加载机制，其实也就是通过进行文本解析，让`python`的方法能够在`yaml`中进行伪调用

7. 断言的封装

   将断言封装在如上内容中，进行解析后，对断言进行判断

   ```yaml
   - assertion:
       equal:
         aa: bb
         gg: brother
       contains:
         - a
         - b
         - c
         - d
         - f
   ```
10. 完成异常处理和日志的封装

11. 多环境下，对`base_url`的封装，并实现根据配置环境自动加载

12. 接口的加密和签名

13. 完成allure生成报告的定制


#### 还需要完成的内容
1. 请求结果用正则表达式的形式进行提取
2. 断言的处理，主要是断言如果不是返回的文本或json，该如何处理，一定要保证断言能够顺利执行，
3. 对于${}的替换，感觉算法不是很完善，应该会有隐藏的bug，前期的递归遍历没有将list考虑进去
4. 对于热加载函数和${}得到的变量，应该支持加减乘除的运算
5. 接口签名和接口加密的内容
6. 将接口测试的框架和web测试的框架整合到一起



`jenkins安装脚本`
```commandline
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo yum upgrade
sudo yum install epel-release java-11-openjdk-devel
sudo yum install jenkins
sudo systemctl daemon-reload
```

