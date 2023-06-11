FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y

COPY requirements.txt /usr/local/src/Azure-OpenAI-Secure-Wrapper/requirements.txt

WORKDIR /usr/local/src/Azure-OpenAI-Secure-Wrapper
RUN pip install -r requirements.txt

COPY python-server-proxy/ /usr/local/src/Azure-OpenAI-Secure-Wrapper/python-server-proxy/

EXPOSE 80
CMD ["python", "python-server-proxy/main.py"]