from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *
from tools_ecomart import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-1106-preview" #mudar aqui

def criar_lista_arquivo_ids():
    lista_ids_arquivos = []
    file_dados = cliente.files.create(
        file=open("dados/dados_ecomart.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_dados.id)

    file_politicas = cliente.files.create(
        file=open("dados/políticas_ecomart.txt", "rb"),
        purpose="assistants"
    )
    lista_ids_arquivos.append(file_politicas.id)

    file_produtos = cliente.files.create(
        file=open("dados/produtos_ecomart.txt","rb"),
        purpose="assistants"
    )

    lista_ids_arquivos.append(file_produtos.id)

    return lista_ids_arquivos

def criar_thread():
    return cliente.beta.threads.create()

def criar_assistente(file_ids=[]):
    assistente = cliente.beta.assistants.create(
        name="Atendente EcoMart",
        instructions = f"""
                Você é um chatbot de atendimento a clientes de um e-commerce. 
                Você não deve responder perguntas que não sejam dados do ecommerce informado!
                Além disso, adote a persona abaixo para respondero ao cliente.
                """,
        model = modelo,
        tools= minhas_tools,
        file_ids=file_ids
    )
    return assistente
