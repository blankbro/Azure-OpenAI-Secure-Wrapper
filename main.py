import os

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from langchain.llms import AzureOpenAI

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', default='World')
    return jsonify({'message': f'Hello, {name}!'})


@app.route('/completion', methods=['POST'])
def completion():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'code': 400, 'msg': 'prompt 参数不能为空'})
    llm = AzureOpenAI(deployment_name=os.getenv("OPENAI_ENGINE_DEPLOYMENT_NAME"))
    response = llm(prompt)
    return jsonify({'code': 200, 'msg': 'success', 'data': response})


# 启动Web服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
