# -*- coding: utf-8 -*-
import json

from flask import Flask, jsonify, request, Response

from langchain_helper import completion as langchain_completion, chat_completion as langchain_chat_completion
from origin_helper import completion as origin_completion, chat_completion as origin_chat_completion

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', default='World')
    return jsonify({'message': f'Hello, {name}!'})


# 创建返回结果为json的response，且json中出现中文时不会被编码
def json_response(json_data):
    response_json_str = json.dumps(json_data, ensure_ascii=False)
    return Response(response_json_str, content_type='application/json')


@app.route('/completion', methods=['POST'])
def completion_api():
    request_body = request.get_json()

    prompt = request_body.get('prompt')
    if not prompt:
        return jsonify({'code': 400, 'msg': 'prompt 参数不能为空'})

    return json_response({'code': 200, 'msg': 'success', 'data': origin_completion(prompt)})


@app.route('/langchain/completion', methods=['POST'])
def langchain_completion_api():
    request_body = request.get_json()

    prompt = request_body.get('prompt')
    if not prompt:
        return jsonify({'code': 400, 'msg': 'prompt 参数不能为空'})

    return json_response({'code': 200, 'msg': 'success', 'data': langchain_completion(prompt)})


@app.route('/chat/completion', methods=['POST'])
def chat_completion_api():
    request_body = request.get_json()

    messages = request_body.get('messages')
    if not messages:
        return jsonify({'code': 400, 'msg': 'messages 参数不能为空'})

    return json_response({'code': 200, 'msg': 'success', 'data': origin_chat_completion(messages)})


@app.route('/langchain/chat/completion', methods=['POST'])
def langchain_chat_completion_api():
    request_body = request.get_json()

    messages = request_body.get('messages')
    if not messages:
        return jsonify({'code': 400, 'msg': 'messages 参数不能为空'})

    return json_response({'code': 200, 'msg': 'success', 'data': langchain_chat_completion(messages)})


# 启动Web服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
