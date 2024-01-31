from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

def send_message(message):
    api_key = os.getenv('GOOGLE_API_KEY')

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    chat = model.start_chat()

    response = chat.send_message(message)

    return response.text

def message_ia():

    return send_message('Crie um texto para motivar pessoas que chamem atenção delas. Crie no maximo 200 letras e sem asteriscos')


def song_name_ia():
    return send_message('me de somente o nome de uma musica pensativa ou sad')