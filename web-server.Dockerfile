FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y

COPY requirements.txt /usr/local/src/Azure-OpenAI-Secure-Wrapper/requirements.txt

WORKDIR /usr/local/src/Azure-OpenAI-Secure-Wrapper
RUN pip install -r requirements.txt

COPY web_server/ /usr/local/src/Azure-OpenAI-Secure-Wrapper/

EXPOSE 80
CMD ["uvicorn", "openai_api_server:app", "--host", "0.0.0.0", "--port", "80"]