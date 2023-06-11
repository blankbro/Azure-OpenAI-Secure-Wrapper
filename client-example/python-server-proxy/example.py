import requests

LOCAL_API_BASE = "http://localhost:80"
SERVER_API_BASE = "http://localhost:8081"
API_BASE = LOCAL_API_BASE


def completion():
    url = f'{API_BASE}/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "你是谁？"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def langchain_completion():
    url = f'{API_BASE}/langchain/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "你是谁？"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def chat_completion():
    url = f'{API_BASE}/chat/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "messages": [{"role": "user", "content": "Hello!"}]
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def langchain_chat_completion():
    url = f'{API_BASE}/langchain/chat/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "messages": [
            {"type": "human", "data": {"content": "你是谁"}}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


if __name__ == "__main__":
    completion()
    langchain_completion()
    chat_completion()
    langchain_chat_completion()
