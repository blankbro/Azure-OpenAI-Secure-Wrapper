set -e

# 删除旧镜像
if docker image ls | grep -q "azure-openai-api-web-server"; then
  docker image rm -f azure-openai-api-web-server
fi

# 打包新镜像
docker build . -f web-server.Dockerfile -t azure-openai-api-web-server

# 停止旧应用
if docker ps -a | grep -q "azure-openai-api-web-server"; then
  docker rm -f azure-openai-api-web-server
fi

# 启动新应用
docker run -d --env-file web-server/.env -p 8089:80 --name azure-openai-api-web-server azure-openai-api-web-server

# 清除未被使用的镜像及其数据
docker image prune -a