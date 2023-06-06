### ChatGPT-API

基于langchain将Azure OpenAI API再进行一层包装，隐藏 OPENAI_API_KEY 等重要信息，只暴露 prompt。

这么做的目的主要是在组织内部提供一个 ChatGPT 的 API 供大家使用，为了避免密钥泄露，专门提供了这个接口。

### 本地部署

Please ensure you have Python 3.9+ installed.

Create `venv` environment for Python:

```console
python -m venv .venv

# 进入虚拟环境
source .venv/bin/activate

# 退出虚拟环境
deactivate
```

Install `PIP` Requirements

```console
pip install -r requirements.txt
```

configure your .env as Environment variables

```
cp .env.template .env
vi .env # or use whatever you feel comfortable with
```

run

```console
python main.py
```

### 服务器部署

```
# 拉取最新代码
git clone https://github.com/timeway/chatgpt-api.git
git pull

# 删除旧镜像
docker image rm -f chatgpt-api

# 打包新镜像
docker build . -f ChatGPT-API.Dockerfile -t chatgpt-api

# 停止旧应用
docker rm -f chatgpt-api

# 启动新应用
docker run -d --env-file .env -p 8089:80 --name chatgpt-api chatgpt-api 

# 清除未被使用的镜像及其数据
docker image prune -a 

```