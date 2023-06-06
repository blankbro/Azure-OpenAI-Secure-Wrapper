FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y
COPY requirements.txt /usr/local/src/chatgpt-api/requirements.txt
WORKDIR /usr/local/src/chatgpt-api
RUN pip install -r requirements.txt
COPY main.py /usr/local/src/chatgpt-api
EXPOSE 80
CMD ["python", "main.py"]