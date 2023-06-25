# 删除旧镜像
docker image rm -f azure-openai-api-web-server

# 打包新镜像
docker build . -f azure-openai-api-web-server.Dockerfile -t azure-openai-api-web-server

# 停止旧应用
docker rm -f azure-openai-api-web-server

# 启动新应用
docker run -d --env-file azure-openai-api-web-server/.env -p 8081:80 --name azure-openai-api-web-server azure-openai-api-web-server

# 清除未被使用的镜像及其数据
docker image prune -a