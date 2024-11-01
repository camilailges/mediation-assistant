import base64
import json
import os
import requests
from dotenv import load_dotenv
from llama_index.llms.deepinfra import DeepInfraLLM
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
import re

from jwt_console import sendEnvelope
from tools import generic, send_message_file, send_signature_instructions

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

llm = DeepInfraLLM(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct",
        api_key="cuDds7vlAFb60oidHyeyL8gvtRmKoKdf",
        temperature=0.5,
        max_tokens=500,
        additional_kwargs={"top_p": 0.9},
    )

# llm = DeepInfraLLM(
#         model="meta-llama/Meta-Llama-3.1-405B-Instruct",
#         api_key="euZJCXbEID98W7xPNFRVKEUNXxmrlLdm",
#         temperature=0.5,
#         max_tokens=500,
#         additional_kwargs={"top_p": 0.9},
#     )

def send_message(message):

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_WAID,
        "type": "text",
        "text": {"preview_url": False, "body": message},
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN,
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response
    
def generate_response(message_body, name):
    print("messageBody: "+message_body)
    
    try:
        chat_store = SimpleChatStore.from_persist_path("chat_store.json")
    except FileNotFoundError:
        chat_store = SimpleChatStore()

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=10000,
        chat_store=chat_store,
        chat_store_key=name,
    )
    try:
        with open("chat_store.json", "r") as f:
            chat_data = json.load(f)
            print("Conteúdo do chat_store.json:")
            print(json.dumps(chat_data, indent=4))
    except Exception as e:
        print(f"Erro ao ler o arquivo chat_store.json: {e}")
    
    sendEnvelope_tool = FunctionTool.from_defaults(sendEnvelope)
    generic_tool = FunctionTool.from_defaults(generic)
    send_message_file_tool = FunctionTool.from_defaults(send_message_file)
    send_signature_instructions_tool = FunctionTool.from_defaults(send_signature_instructions)

    context = """O Grupo Mediar é uma empresa de mediação extrajudicial que tem forte atuação com inadimplência em escolas. Você é um assistente de WhatsApp do Grupo Mediar, que atua no pós-acordo, ou seja, o acordo entre as partes (escola e pais/alunos inadimplentes) já foi configurado por intermédio dos mediadores. Você auxiliará as pessoas inadimplentes com questões como: retirada de dúvidas gerais a respeito do acordo (forma e data de pagamento, valor acordado, quantidade de parcelas, e o que mais constar no acordo) e informar as instruções para assinatura digital pela plataforma do DocuSign. Também é capaz de fazer o envio do acordo para assinatura por e-mail e fazer o envio do boleto por WhatsApp (caso a forma de pagamento descrita no acordo for boleto). Seja reativo às solicitações do usuário e sempre pense no que fazer, não invoke nenhuma ferramenta se não for necessária. Só acione ferramentas se a mensagem indicar uma pergunta ou pedido direto. Responda a mensagens de saudações apenas com uma saudação de volta, sendo gentil e oferecendo ajuda, e não acione nenhuma ação adicional.
    """
    agent = ReActAgent.from_tools([sendEnvelope_tool, send_message_file_tool, send_signature_instructions_tool, generic_tool], llm=llm, verbose=True, context=context, memory=chat_memory)
    
    response = agent.chat(
        name+": "+message_body
    )

    chat_store.persist(persist_path="chat_store.json")
    try:
        with open("chat_store.json", "r") as f:
            chat_data = json.load(f)
            print("Conteúdo do chat_store.json:")
            print(json.dumps(chat_data, indent=4))
    except Exception as e:
        print(f"Erro ao ler o arquivo chat_store.json: {e}")

    print(str(response))
    return str(response)


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text