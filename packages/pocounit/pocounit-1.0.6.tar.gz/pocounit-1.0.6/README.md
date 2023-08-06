# PocoUnit (unittest framework)

可配合airtest和poco使用的单元测试框架。规范了脚本编写的格式，提供流式日志（stream log）记录服务，然后可以使用[PocoResultPlayer](http://git-qa.gz.netease.com/maki/PocoTestResultPlayer)将运行的内容回放。

## 用法

首先需要继承基类PocoTestCase实现项目组自己的GxxTestCase，在GxxTestCase预处理中将需要用到的对象准备好（包括实例化hunter和poco和动作捕捉），以后在其余用例中继承GxxTestCase即可。

基本用法可参考一下代码模板。

```python
# coding=utf-8

from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker
from pocounit.addons.hunter.runtime_logging import AppRuntimeLogging

from hunter_cli import Hunter, open_platform
from poco.vendor.airtest import AirtestPoco


class GxxTestCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(GxxTestCase, cls).setUpClass()

        # 使用hunter请用此标准格式获取tokenid即可
        tokenid = open_platform.get_api_token('gxx-poco-test')

        # 下面两个对象根据实际情况实例化一下
        cls.hunter = Hunter(tokenid, 'g62', devid='g62_at_408d5c117d0f')
        cls.poco = AirtestPoco('g62', cls.hunter)

        # 启用动作捕捉(action tracker)和游戏运行时日志捕捉插件(runtime logger)
        action_tracker = ActionTracker(cls.poco)
        runtime_logger = AppRuntimeLogging(cls.hunter)
        cls.register_addin(action_tracker)
        cls.register_addin(runtime_logger)
```

然后可以开始编写自己的testcase

```python
# coding=utf8

from ... import GxxTestCase


# 一个文件里建议就只有一个TestCase
# 一个Case做的事情尽量简单，不要把一大串操作都放到一起
class MyTestCase(GxxTestCase):     
    def setUp(self):
        # 可以调用一些前置条件指令和预处理指令
        self.hunter.script('print 23333', lang='python')

    def runTest(self):
        # 函数名就是这个，用其他名字无效

        # 普通语句跟原来一样
        self.poco(text='角色').click()
        
        # 断言语句跟python unittest写法一模一样
        self.assertTrue(self.poco(text='最大生命').wait(3).exists(), "看到了最大生命")

        self.poco('btn_close').click()
        self.poco('movetouch_panel').offspring('point_img').swipe('up')

    def tearDown(self):
        # 如果没有清场操作，这个函数就不用写出来
        pass

    # 不要写以test开头的函数，除非你知道会发生什么
    # def test_xxx():
    #     pass


if __name__ in ('__main__', 'airtest.cli.runner'):
    import pocounit
    pocounit.main() 

```


### Airtest环境中hunter与poco对象的初始化

使用AirtestIDE或者Testlab时可以用一下方式初始化hunter和poco对象

```
from airtest_hunter import AirtestHunter, open_platform

apitoken = open_platform.get_api_token()
hunter = AirtestHunter(apitoken, 'g47')  # 只需要传入项目代号(process)
poco = AirtestPoco('g47', hunter)
```
