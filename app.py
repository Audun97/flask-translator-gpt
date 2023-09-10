import openai
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def translator():
    if request.method == "POST":
        input_language = request.form["input_language"]
        output_language = request.form["output_language"]
        formal_pronouns_checkbox = request.form.get("formal_pronouns", "")
        user_input = request.form["user_input"]

        if output_language == "German":
            if formal_pronouns_checkbox == "1":
                formal_pronouns = "Use formal pronouns. E.g. \"Sie\" instead of \"du\" and \"Ihnen\" instead of \"dir\"."
            else:
                formal_pronouns = "Use informal pronouns. E.g. \"du\" instead of \"Sie\" and \"dir\" instead of \"Ihnen\"."
        else:
            formal_pronouns = ""

        # Create the prompt for the GPT-4 model
        system_prompt = f"You are a helpful translator specializing in translating {input_language} to {output_language}. What makes you great is that you do NOT translate word for word. Instead you translate the meaning. You utilize things like paraphrasing, reformulation and the introduction of figures of speech common in {output_language}. I.e. it should sound like natural {output_language}. One should not even be able to tell that is was not originally written in {input_language}. Be creative. {formal_pronouns}."

        # Use the OpenAI API to generate the response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        ) 
        
        # Extract the assistant's message from the response. I had to add a comment to make vscode ignore a warning that response was not a dictionary
        assistant_message = response['choices'][0]['message']['content'] # type: ignore[reportGeneralTypeIssues]

        return render_template("index.html", response=assistant_message, user_input=user_input)

    return render_template("index.html", user_input="")

if __name__ == "__main__":
    app.run(debug=True)