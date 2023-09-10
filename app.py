from flask import Flask, render_template, request
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful translator specializing in translating {input_language} to {output_language}. What makes you great is that you do NOT translate word for word. Instead you translate the meaning. You utilize things like paraphrasing, reformulation and the introduction of figures of speech common in {output_language}. I.e. it should sound like natural {output_language}. One should not even be able to tell that is was not originally written in {input_language}. Be creative. {formal_pronouns}"),
    ("human", "{text}"),
])

# Initialize the OpenAI LLM
llm = ChatOpenAI(model='gpt-4', temperature=0.9)

# LLMChain initialization with the prompt template and llm model
chain = LLMChain(llm=llm, prompt=prompt_template)

# Flask app initialization
app = Flask(__name__)

# This specifies the route for the app and which HTTP methods allowed for this route. 
# The route is the URL path that you can visit in your browser. 
@app.route("/", methods=["GET", "POST"])

def translator():
    # Post request is handled by the form. This is the form submission.
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

        response = chain.run({'output_language': output_language, 'input_language': input_language, 'formal_pronouns': formal_pronouns,  'text': user_input})
        return render_template("index.html", response=response, user_input=user_input)

    # Get request is handled by render_template. This is the initial page load.
    return render_template("index.html", user_input="")

# Checks if the script is being run directly (not imported as a module).
if __name__ == "__main__":
    app.run(debug=True)