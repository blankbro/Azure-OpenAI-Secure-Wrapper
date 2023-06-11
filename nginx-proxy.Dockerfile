FROM nginx:1.25.0

COPY nginx-proxy/azure-openai-api-proxy.conf.template /etc/nginx/templates/azure-openai-api-proxy.conf.template

RUN rm -rf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]