import base64
import json
import os
import requests
from dotenv import load_dotenv
from llama_index.llms.deepinfra import DeepInfraLLM
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
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
    
    sendEnvelope_tool = FunctionTool.from_defaults(sendEnvelope)
    generic_tool = FunctionTool.from_defaults(generic)
    send_message_file_tool = FunctionTool.from_defaults(send_message_file)
    send_signature_instructions_tool = FunctionTool.from_defaults(send_signature_instructions)

    context = """O Grupo Mediar é uma empresa de mediação extrajudicial que tem forte atuação com inadimplência em escolas. Você é um assistente de WhatsApp do Grupo Mediar, que atua no pós-acordo, ou seja, o acordo entre as partes (escola e pais/alunos inadimplentes) já foi configurado por intermédio dos mediadores. Você auxiliará as pessoas inadimplentes com questões como: retirada de dúvidas gerais a respeito do acordo (data de pagamento, forma de pagamento, etc.), envio do acordo para assinatura por e-mail, envio de instruções para assinatura digital pela plataforma do DocuSign e envio do boleto por WhatsApp, caso a forma de pagamento descrita no acordo for boleto. Seja reativo às solicitações do usuário e sempre pense no que fazer, não invoke nenhuma ferramenta se não for necessária
    """
    # context = """Você é um assistente de mediação extrajudicial da empresa Grupo Mediar. A pessoa Mariana dos Santos vai entrar em contato contigo para tirar dúvidas a respeito do documento. Seja reativo às solicitações do usuário e sempre pense no que fazer, não invoke nenhuma ferramenta se não for necessária.
    # """
    agent = ReActAgent.from_tools([sendEnvelope_tool, send_message_file_tool, send_signature_instructions_tool, generic_tool], llm=llm, verbose=True, context=context)
    
    response = agent.chat(
        name+": "+message_body
    )

    print(str(response))
    return str(response)


# def anwserOnDocument(message_body):
#     """Você é um assistente de mediação extrajudicial da empresa Grupo Mediar. A pessoa Mariana dos Santos vai entrar em contato contigo para tirar dúvidas a respeito do documento abaixo e você deve responder de acordo com o documento somente. Caso ela lhe questione a respeito de algo fora do contrato não responda.
#     Contrato: Data: 26/08/2024 Hora: 10h \n TERMO DE ACORDO \n Conciliadora e Mediadora Extrajudicial Maria da Costa \n Conciliandos / Mediandos \n Mariana dos Santos, 235.728.500-30, representante financeira da aluna Luiza Santos, matrícula 23300101. Contato telefônico: 51.985074177. \n Laurindo Oliveira, CPF 766.215.650-53, Diretor Presidente do Colégio Romano Santa Marta, da Associação Dom Edmundo Luis Kunz, inscrita no CNPJ sob o no 01.066.367/0001-70, entidade filantrópica, com sede na Rua Noel Rosa, 1933, CEP 91210-110, no município de Porto Alegre/RS. \n Aberta a sessão, apresentados os objetivos e princípios do método da conciliação, houve aceite na participação. Estabelecido um diálogo produtivo, chegou-se ao seguinte entendimento: \n Mariana dos Santos está ciente de sua dívida com a respectiva escola, referente aos meses de março a agosto de 2024, no valor atualizado de R$ 7.818,48. Na presente sessão, foi negociada a seguinte forma de quitação: \n - 02 parcelas de R$ 3.909,24, via boleto bancário, nos dias 20/10 e 10/11. \n Considera-se cumprido este acordo após a quitação integral do valor pendente acima referido, relativo ao contrato de prestação de serviço educacional estabelecido entre as partes. O presente acordo constitui título executivo extrajudicial, podendo ser executado judicialmente. \n Mariana dos Santos– Medianda \n Laurindo Oliveira - Diretor Presidente \n Maria da Costa - Conciliadora/Mediadora"
#     """

#     print("anwserOnDocument")
    
#     prompt = """Você é um assistente de mediação extrajudicial da empresa Grupo Mediar. A pessoa Mariana dos Santos vai entrar em contato contigo para tirar dúvidas a respeito do documento abaixo e você deve responder de acordo com o documento somente. Caso ela lhe questione a respeito de algo fora do contrato não responda.
#     Contrato: Data: 26/08/2024 Hora: 10h \n TERMO DE ACORDO \n Conciliadora e Mediadora Extrajudicial Maria da Costa \n Conciliandos / Mediandos \n Mariana dos Santos, 235.728.500-30, representante financeira da aluna Luiza Santos, matrícula 23300101. Contato telefônico: 51.985074177. \n Laurindo Oliveira, CPF 766.215.650-53, Diretor Presidente do Colégio Romano Santa Marta, da Associação Dom Edmundo Luis Kunz, inscrita no CNPJ sob o no 01.066.367/0001-70, entidade filantrópica, com sede na Rua Noel Rosa, 1933, CEP 91210-110, no município de Porto Alegre/RS. \n Aberta a sessão, apresentados os objetivos e princípios do método da conciliação, houve aceite na participação. Estabelecido um diálogo produtivo, chegou-se ao seguinte entendimento: \n Mariana dos Santos está ciente de sua dívida com a respectiva escola, referente aos meses de março a agosto de 2024, no valor atualizado de R$ 7.818,48. Na presente sessão, foi negociada a seguinte forma de quitação: \n - 02 parcelas de R$ 3.909,24, via boleto bancário, nos dias 20/10 e 10/11. \n Considera-se cumprido este acordo após a quitação integral do valor pendente acima referido, relativo ao contrato de prestação de serviço educacional estabelecido entre as partes. O presente acordo constitui título executivo extrajudicial, podendo ser executado judicialmente. \n Mariana dos Santos– Medianda \n Laurindo Oliveira - Diretor Presidente \n Maria da Costa - Conciliadora/Mediadora"
#     """

#     messages = [
#         ChatMessage(role="system", content=prompt),
#         ChatMessage(role="user", content="Mariana: "+message_body),
#     ]
    
#     content = ""
#     for chat_response in llm.stream_chat(messages):
#         content += chat_response.message.content

#     print(chat_response.message.content, end="")
    # return chat_response.message.content

# def generate_response(message_body):
#     print("messageBody: "+message_body)

#     question = """Você é um assistente de mediação extrajudicial da empresa Grupo Mediar. A pessoa Mariana dos Santos vai entrar em contato contigo para tirar dúvidas a respeito do documento abaixo e você deve responder de acordo com o documento somente. Caso ela lhe questione a respeito de algo fora do contrato não responda.
#     Contrato: Data: 26/08/2024 Hora: 10h \n TERMO DE ACORDO \n Conciliadora e Mediadora Extrajudicial Maria da Costa \n Conciliandos / Mediandos \n Mariana dos Santos, 235.728.500-30, representante financeira da aluna Luiza Santos, matrícula 23300101. Contato telefônico: 51.985074177. \n Laurindo Oliveira, CPF 766.215.650-53, Diretor Presidente do Colégio Romano Santa Marta, da Associação Dom Edmundo Luis Kunz, inscrita no CNPJ sob o no 01.066.367/0001-70, entidade filantrópica, com sede na Rua Noel Rosa, 1933, CEP 91210-110, no município de Porto Alegre/RS. \n Aberta a sessão, apresentados os objetivos e princípios do método da conciliação, houve aceite na participação. Estabelecido um diálogo produtivo, chegou-se ao seguinte entendimento: \n Mariana dos Santos está ciente de sua dívida com a respectiva escola, referente aos meses de março a agosto de 2024, no valor atualizado de R$ 7.818,48. Na presente sessão, foi negociada a seguinte forma de quitação: \n - 02 parcelas de R$ 3.909,24, via boleto bancário, nos dias 20/10 e 10/11. \n Considera-se cumprido este acordo após a quitação integral do valor pendente acima referido, relativo ao contrato de prestação de serviço educacional estabelecido entre as partes. O presente acordo constitui título executivo extrajudicial, podendo ser executado judicialmente. \n Mariana dos Santos– Medianda \n Laurindo Oliveira - Diretor Presidente \n Maria da Costa - Conciliadora/Mediadora"
#     """

#     messages = [
#         ChatMessage(role="system", content=question),
#         ChatMessage(role="user", content="Mariana: "+message_body),
#     ]
    
#     content = ""
#     for chat_response in llm.stream_chat(message_body, messages):
#         content += chat_response.message.content

#     print(chat_response.message.content, end="")
#     return chat_response.message.content

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