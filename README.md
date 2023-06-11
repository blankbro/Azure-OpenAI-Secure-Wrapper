# Azure OpenAI Secure Wrapper

Azure OpenAI 安全的包装者，旨在隐藏 OPENAI_API_KEY 和 OPENAI_API_BASE 等重要信息，给他人或组织内部提供 OpenAI 服务。

本项目提供了两种方式： python-server-proxy 和 nginx-proxy

## Python Server Proxy

Python 编写的一个 WEB 服务，prompt 从 HTTP 请求中获取，OPENAI_API_KEY 和 OPENAI_API_BASE 从环境变量中获取，然后调用 OpenAI API，最后将结果包装返回。

### Local Run

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
cp python-server-proxy/.env.template python-server-proxy/.env
vi python-server-proxy/.env # or use whatever you feel comfortable with
```

start

```console
python python-server-proxy/main.py
```

### Docker Run

configure your .env as Environment variables

```
cp python-server-proxy/.env.template python-server-proxy/.env
vi python-server-proxy/.env # or use whatever you feel comfortable with
```

run

```
sh python-server-proxy-start.sh
```

### Client Example / Test

See [client-example/python-server-proxy/example.py](client-example/python-server-proxy/example.py)

## Nginx Proxy

通过配置 Nginx 代理 OpenAI 接口，隐藏 OPENAI_API_KEY 和 OPENAI_API_BASE 等重要信息。

### Docker Run

configure your .env as Environment variables

```
cp nginx-proxy/.env.template nginx-proxy/.env
vi nginx-proxy/.env # or use whatever you feel comfortable with
```

start

```
sh nginx-proxy-start.sh
```

### Client Example / Test

See [client-example/nginx-proxy/langchain_example.py](client-example/nginx-proxy/langchain_example.py) (langchain 版本)

See [client-example/nginx-proxy/origin_example.py](client-example/nginx-proxy/origin_example.py) (openai python sdk 版本)

langchain 版本 和 openai python sdk 版本，任选其一即可。