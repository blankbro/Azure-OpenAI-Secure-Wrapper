# 删除旧镜像
docker image rm -f azure-openai-api-python-server-proxy

# 打包新镜像
docker build . -f azure-openai-api-python-server-proxy.Dockerfile -t azure-openai-api-python-server-proxy

# 停止旧应用
docker rm -f azure-openai-api-python-server-proxy

# 启动新应用
docker run -d --env-file azure-openai-api-python-server-proxy/.env -p 8081:80 --name azure-openai-api-python-server-proxy azure-openai-api-python-server-proxy

# 清除未被使用的镜像及其数据
docker image prune -a