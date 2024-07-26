# 使用官方的 Python 基础镜像
FROM python:3.9-slim

# 更换 apt 源为清华源，并安装基础包
RUN apt-get install -y apt-transport-https ca-certificates \
 && sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources \
 && apt-get update \
 && apt-get upgrade -y \
 && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /test

# 复制项目到工作目录
COPY . .

# 使用清华源更新 pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip install --upgrade pip

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 playwright chrome 浏览器
# RUN playwright install chrome

# 指定默认测试文件 test_demo.py 可以在 docker run 里指定测试文件
ENV case=test_main.py
ENV csv=test_main.csv
ENV scope=dev,test,stage,smoke

# 运行 pytest
CMD ["sh", "-c", "pytest -vs cases/$case --csv=src/script/$csv --scope=$scope"]
