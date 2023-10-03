import requests
import json
import sseclient
from dotenv import load_dotenv
import os
from flask import Flask, Response

# Load environment variables from .env file
load_dotenv()
 
API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/stream')
def performRequestWithStreaming():
    reqUrl = 'https://api.openai.com/v1/completions'
    reqHeaders = {
        'Accept': 'text/event-stream',
        'Authorization': 'Bearer ' + API_KEY
    }
    reqBody = {
      "model": "text-davinci-003",
      "prompt": "How many Germans does oit take to change a lightbulb?",
      "max_tokens": 100,
      "temperature": 0,
      "stream": True,
    }
    request = requests.post(reqUrl, stream=True, headers=reqHeaders, json=reqBody)
    client = sseclient.SSEClient(request)

    def generate():
        for event in client.events():
            if event.data != '[DONE]':
                yield json.loads(event.data)['choices'][0]['text']
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    performRequestWithStreaming()