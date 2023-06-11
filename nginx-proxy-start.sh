docker image rm -f azure-openai-api-nginx-proxy

docker build . -f nginx-proxy.Dockerfile -t azure-openai-api-nginx-proxy

docker rm -f azure-openai-api-nginx-proxy

docker run -d --env-file nginx-proxy/.env -p 8080:80 --name azure-openai-api-nginx-proxy azure-openai-api-nginx-proxy

# 清除未被使用的镜像及其数据
#docker image prune -a
