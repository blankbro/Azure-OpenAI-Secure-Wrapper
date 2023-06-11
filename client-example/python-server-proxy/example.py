import requests


def completion():
    url = 'http://localhost:8089/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "你是谁？"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def langchain_completion():
    url = 'http://localhost:8089/langchain/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": "你是谁？"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def chat_completion():
    url = 'http://localhost:8089/chat/completion'
    headers = {'Content-Type': 'application/json'}
    data = {
        "messages": [{"role": "user", "content": "Hello!"}]
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def langchain_chat_completion():
    url = 'http://localhost:8089/langchain/chat/completion'
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
