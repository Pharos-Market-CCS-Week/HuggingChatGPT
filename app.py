# LIBRERIA DE DOTENV
import os
from dotenv import find_dotenv, load_dotenv

# LIBRERIA DE CHAT GPT
from hugchat import hugchat
from hugchat.login import Login

# FLASK
from flask import Flask, request
app = Flask(__name__)

load_dotenv(find_dotenv())
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Log in to huggingface and grant authorization to huggingchat
sign = Login(EMAIL, PASSWORD)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

@app.route("/chat", methods=["POST"])
def huggingChat():

    # non stream response
    msg = request.get_json()
    query = msg["message"]

    print("HACIENDO UNA CONSULTA: ", query)
    query_result = chatbot.query(query)
    print("RESULTADO: ", query_result) # or query_result.text or query_result["text"]

    # Create a new conversation
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)

    # Get conversation list
    # conversation_list = chatbot.get_conversation_list()

    # Switch model to the given index
    chatbot.switch_llm(0) # Switch to the first model

    # Get information about the current conversation
    # info = chatbot.get_conversation_info()

    # Get conversations on the server that are not from the current session (all your conversations in huggingchat)
    chatbot.get_remote_conversations(replace_conversation_list=True)

    response = {
        "respuesta" : str(query_result)
    }

    return {'response': response, 'status': 200}

