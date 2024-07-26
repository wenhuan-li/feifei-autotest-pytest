### 构建
```
docker build -t feifei-autotest-linux .
```

### 启动

#### 测试 Hello
```
docker run --rm feifei-autotest-linux
```

#### 指定脚本文件、模块文件、测试范围

- 测试前, 需要将指定文件放入当前项目的suites目录中
- 脚本文件: 建议与测试文件同名, 文件包含用例id、名称、参数、预期等, 文件名规则 test_xxx_xxx.csv
- 模块文件: 代表测试的具体方法, 定义具体测试的动作. 接口测试中可以定义接口请求和验证; 界面测试可以定义界面操作和验证
- 测试范围: 默认包含dev, test, stage, smoke
```
windows:
docker run --rm -v %cd%\mods:/test/mods -v %cd%\script:/test/script -e csv=test_main.csv -e scope=dev feifei-autotest-linux

linux:
docker run --rm -v /mods:/test/mods -v /script:/test/script -e csv=test_main.csv -e scope=dev feifei-autotest-linux
```

#### 解释
- -v %cd%\mods:/test/mods | -v /mods:/test/mods：将当前目录下的 mods 目录挂载到 Docker 容器中的 /test/mods 目录. 
- -v %cd%\script:/test/script | v /script:/test/script：将当前目录下的 script 目录挂载到 Docker 容器中的 /test/script 目录. 
- -e csv=test_main.csv：默认执行test_main.csv文件中的用例, 可以直接修改它或上传并指定自定义文件
- -e scope=dev：默认全环境执行, 包括但不限于：dev, test, stage, smoke
- {my_project_image}：Docker 镜像的名称. 

#### 调试
```
启动容器但不执行任何实际工作
docker run -d feifei-autotest-linux tail -f /dev/null

进入运行中的容器调试
docker exec -it <container_id> /bin/sh
```