import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

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
    
def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_message_file(name, **kwargs):
    f"""Envia o arquivo do boleto para pagamento por WhatsApp para {name}
    args:
        None
    """
    print("send_message_file")

    docPath = 'Boleto.pdf'
    fileName = "Boleto.pdf"

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_WAID,
        "type": "document",
        "document": {
        "id": "8609902529078544",
        "filename": fileName
    }
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
    
def generic(**kwargs):
    """Este é um modelo de linguagem genérico que pode responder a qualquer pergunta sobre não tratada por nenhuma outra ferramenta fornecida. Você deve responder de acordo com o documento/contrato a seguir somente. Caso ela lhe questione a respeito de algo fora do contrato não responda.
    Contrato: Data: 26/08/2024 Hora: 10h \n TERMO DE ACORDO \n Conciliadora e Mediadora Extrajudicial Maria da Costa \n Conciliandos / Mediandos \n Mariana dos Santos, 235.728.500-30, representante financeira da aluna Luiza Santos, matrícula 23300101. Contato telefônico: 51.985074177. \n Laurindo Oliveira, CPF 766.215.650-53, Diretor Presidente do Colégio Romano Santa Marta, da Associação Dom Edmundo Luis Kunz, inscrita no CNPJ sob o no 01.066.367/0001-70, entidade filantrópica, com sede na Rua Noel Rosa, 1933, CEP 91210-110, no município de Porto Alegre/RS. \n Aberta a sessão, apresentados os objetivos e princípios do método da conciliação, houve aceite na participação. Estabelecido um diálogo produtivo, chegou-se ao seguinte entendimento: \n Mariana dos Santos está ciente de sua dívida com a respectiva escola, referente aos meses de março a agosto de 2024, no valor atualizado de R$ 7.818,48. Na presente sessão, foi negociada a seguinte forma de quitação: \n - 02 parcelas de R$ 3.909,24, via boleto bancário, nos dias 20/10 e 10/11. \n Considera-se cumprido este acordo após a quitação integral do valor pendente acima referido, relativo ao contrato de prestação de serviço educacional estabelecido entre as partes. O presente acordo constitui título executivo extrajudicial, podendo ser executado judicialmente. \n Mariana dos Santos– Medianda \n Laurindo Oliveira - Diretor Presidente \n Maria da Costa - Conciliadora/Mediadora""
    args:
        None
    """
    return 200

def send_signature_instructions(name, **kwargs):
    f"""Realizar assinatura digital por meio de plataformas como Docusign não é algo trivial para muitas pessoas que tem um pouco mais de dificuldade de mexer com aparelhos eletrônicos. Portanto, caso {name} tenha dúvidas sobre como fazer a assinatura digital, a ferramenta envia as instruções para fazer a assinatura digital. Assuma que o usuário já recebeu o acordo para assinatura, e portanto ela só quer as instruções. Se ela precisar que envie novamente o acordo, ela pedirá. Por isso não invoca nenhuma outra ferramenta após, sem que seja necessário.
    args:
        None
    """
    
    send_message(f"Entendi, {name}. Vou te enviar instruções para realizares a assinatura digital.")
    send_message("1. Abra o seu aplicativo do email\n 2. Clica no link do Docusign\n 3. Clique em \"Assinar\" no canto superior direito\n 4. Preencha seus dados\n 5. Pronto")
    send_message("Caso continues com dúvidas me avise")

    return 200