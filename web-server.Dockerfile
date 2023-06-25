FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y

COPY requirements.txt /usr/local/src/Azure-OpenAI-Secure-Wrapper/requirements.txt

WORKDIR /usr/local/src/Azure-OpenAI-Secure-Wrapper
RUN pip install -r requirements.txt

COPY web_server/ /usr/local/src/Azure-OpenAI-Secure-Wrapper/web-server/

EXPOSE 80
CMD ["python", "web_server/opanai_api_server.py"]