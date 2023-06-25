# Azure OpenAI Secure Wrapper

Azure OpenAI 安全的包装者，旨在隐藏 OPENAI_API_KEY 和 OPENAI_API_BASE 等重要信息，给他人或组织内部提供 OpenAI 服务。

本项目提供了两种方式： Web server 和 Nginx proxy

## Web server

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
cp web_server/.env.template web_server/.env
vi web_server/.env # or use whatever you feel comfortable with
```

start

```console
uvicorn openai_api_server:app --host 0.0.0.0 --port 80
```

### Docker Run

configure your .env as Environment variables

```
cp web_server/.env.template web_server/.env
vi web_server/.env # or use whatever you feel comfortable with
```

run

```
sh web-server-start.sh
```

### Client Example / Test

See [client-example/web_server/example.py](client-example/web_server/example.py)

## Nginx Proxy

通过配置 Nginx 代理 OpenAI 接口，隐藏 OPENAI_API_KEY 和 OPENAI_API_BASE 等重要信息。

### Docker Run

configure your .env as Environment variables

```
cp nginx_proxy/.env.template nginx_proxy/.env
vi nginx_proxy/.env # or use whatever you feel comfortable with
```

start

```
sh nginx_proxy-start.sh
```

### Client Example / Test

See [client_example/nginx_proxy/langchain_example.py](client_example/nginx_proxy/langchain_example.py) (langchain 版本)

See [client_example/nginx_proxy/openai_api_example.py](client_example/nginx_proxy/openai_api_example.py) (openai python sdk 版本)

langchain 版本 和 openai python sdk 版本，任选其一即可。