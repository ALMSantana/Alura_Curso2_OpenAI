from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_documento import *
from selecionar_persona import *
from assistentes_ecomart import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview"

app = Flask(__name__)
app.secret_key = 'alura'


thread = criar_thread()
file_ids = criar_lista_arquivo_ids() #adiciona aqui
assistente = criar_assistente()


def bot(prompt):
    maxima_repeticao = 1
    repeticao = 0
    while True:
        try:
            personalidade = personas[selecionar_persona(prompt)]

            # adiciona aqui
            cliente.beta.threads.messages.create(
                thread_id=thread.id, 
                role = "user",
                content =  f"""
                Assuma, de agora em diante, a personalidade abaixo. 
                Ignore as personalidades anteriores.

                # Persona
                {personalidade}
                """
            )

            #mudar aqui
            cliente.beta.threads.messages.create(
                thread_id=thread.id, 
                role = "user",
                content =  prompt,
                file_ids=file_ids
            )

            run = cliente.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistente.id
            )

            while run.status !="completed":
                run = cliente.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
            )

            historico = list(cliente.beta.threads.messages.list(thread_id=thread.id).data)
            resposta = historico[0]
            return resposta
        except Exception as erro:
                repeticao += 1
                if repeticao >= maxima_repeticao:
                        return "Erro no GPT: %s" % erro
                print('Erro de comunicação com OpenAI:', erro)
                sleep(1)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt = prompt)
    texto_resposta = resposta.content[0].text.value
    return texto_resposta

if __name__ == "__main__":
    app.run(debug = True)
