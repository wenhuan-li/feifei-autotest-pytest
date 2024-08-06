

## 使用

```
pytest -vs --csv=script/test_main.csv --slowtime=1000 --headless --alluredir=target/allure-results
```

### 说明
- --csv: 测试用例脚本, 其中包含测试标题, 步骤, 描述, 参数, 其他开关. 参考[测试用例脚本](#script)
- --slowtime: BS界面测试时每一步操作的间隔时间, 单位毫秒
- --headless: BS界面测试时开启无头模式, 即不开启浏览器
- --alluredir: allure-results生成的目录

## 测试用例脚本<a id="script" />
```Excel
case_id,case_name,step_id,step_name,method,route,parameter,hard_assert,scope
0001,Test hello,1,Print hello,test_http_api,hello.hello.print_hello,,false,dev
```

### 说明
- case_id -> str: 用例编号
- case_name -> str: 用例名称
- step_id -> str: 步骤编号
- step_name -> str: 步骤说明
- method -> str: 要使用的测试方法
  - test_http_api: http接口测试方法
  - test_page_gui: bs应用的界面测试方法
  - test_app_gui: cs应用的界面测试方法
- route -> str: module路径.类名.方法, 全部小写
- parameter -> str: 测试参数
- hard_assert -> bool: 是否硬断言, 选项: false, true
- scope -> str: 测试范围, 默认全范围: smoke, dev, test, stage 
