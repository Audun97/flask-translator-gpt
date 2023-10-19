from flask import Flask, Response, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
import requests
import json
import sseclient

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from an environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translator():
        data = request.get_json()
        session['data'] = data  # Store the data in the session
        return jsonify({"status": "success"}), 200

@app.route("/update", methods=["GET"])
def updates():
    data = session.get('data')  # Retrieve the data from the session
    input_language = data["input_language"]
    output_language = data["output_language"]
    formal_pronouns_checkbox = data.get("formal_pronouns", "")
    user_input = data["user_input"]
    if output_language == "German":
        if formal_pronouns_checkbox == "1":
            formal_pronouns = "Use formal pronouns. E.g. \"Sie\" instead of \"du\" and \"Ihnen\" instead of \"dir\"."
        else:
            formal_pronouns = "Use informal pronouns. E.g. \"du\" instead of \"Sie\" and \"dir\" instead of \"Ihnen\"."
    else:
        formal_pronouns = ""

    # Create the prompt for the GPT-4 model
    system_prompt = f"You are a helpful translator specializing in translating {input_language} to {output_language}. What makes you great is that you do NOT translate word for word. Instead you translate the meaning. You utilize things like paraphrasing, reformulation and the introduction of figures of speech common in {output_language}. I.e. it should sound like natural {output_language}. One should not even be able to tell that is was not originally written in {input_language}. Be creative. {formal_pronouns}."

    reqUrl = 'https://api.openai.com/v1/chat/completions'
    reqHeaders = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + API_KEY
    }
    #Possible models: gpt-3.5-turbo, gpt-4 etc
    reqBody = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "stream": True,
        "temperature": 0,
    }
    response = requests.post(reqUrl, stream=True, headers=reqHeaders, json=reqBody)
    client = sseclient.SSEClient(response)

    def generate():
        for event in client.events():
            if event.data != '[DONE]':
                event_data = json.loads(event.data)
                if 'choices' in event_data and event_data['choices'] and 'delta' in event_data['choices'][0] and 'content' in event_data['choices'][0]['delta']:
                    yield 'data: {}\n\n'.format(event_data['choices'][0]['delta']['content'])
            else:
                yield 'data: END\n\n'
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    if os.getenv('FLASK_ENV') != 'production':
        app.run(debug=True)