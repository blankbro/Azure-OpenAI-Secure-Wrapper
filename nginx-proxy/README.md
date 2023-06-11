# Nginx Proxy

通过 Nginx 代理 Azure Open AI API，隐藏 OPENAI_API_KEY 等重要信息，给组织内部使用。

Through Nginx proxy Azure Open AI API, important information such as OPENAI_API_KEY is hidden for internal use of the organization.

## Run Nginx Proxy

configure your .env as Environment variables

```
cp .env.template .env
vi .env # or use whatever you feel comfortable with
```

run
```
./start.sh
```

## Use Nginx Proxy

See [example.py](client-example/nginx-proxy/example.py)

See [langchain-example.py](client-example/nginx-proxy/langchain-example.py)
