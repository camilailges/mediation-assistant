import os
from flask import jsonify
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
    f"""Envia o arquivo do boleto para pagamento para {name}, por meio da ferramenta de conversa WhatsApp (ou seja, não por e-mail)
    args:
        name: nome do usuário
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
        "id": "528247256787521",
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
        return jsonify({"status": "OK"}), 200, response
    else:
        print(response.status_code)
        print(response.text)
        return response
    
def generic(**kwargs):
    """Este é um modelo de linguagem genérico que pode responder a qualquer pergunta feita por um usuário não tratada por nenhuma outra ferramenta fornecida. Você deve responder de acordo com o documento/contrato a seguir somente, como responder perguntas sobre forma e data de pagamento, valor acordado, quantidade de parcelas, e o que mais constar no acordo. Caso o usuário questione algo que não esteja no contrato não responda. Depois que responder o usuário, não invoca nenhuma outra ferramenta sem que o usuário peça. Só acione alguma ferramenta depois se a mensagem indicar uma pergunta ou pedido direto.
    Contrato: Data: 26/08/2024 Hora: 10h \n TERMO DE ACORDO \n Conciliadora e Mediadora Extrajudicial Fulana de Tal \n Conciliandos / Mediandos \n Camila dos Santos Ilges, 123.123.123-12, representante financeira da aluna Ciclana dos Santos, matrícula 12322123. Contato telefônico: 51.9911111-22. \n Fulano Costa, CPF 111.111.111-11, Diretor Presidente do Colégio São João, inscrito no CNPJ sob o no 00.000.000/0000-00, entidade filantrópica, com sede na Rua das Flores, 1234, CEP 00000-000, no município de Porto Alegre/RS. \n Aberta a sessão, apresentados os objetivos e princípios do método da conciliação, houve aceite na participação. Estabelecido um diálogo produtivo, chegou-se ao seguinte entendimento: \n Camila Ilges dos Santos está ciente de sua dívida com a respectiva escola, referente aos meses de março a agosto de 2024, no valor atualizado de R$ 7.818,48. Na presente sessão, foi negociada a seguinte forma de quitação: \n - 02 parcelas de R$ 3.909,24, via boleto bancário, nos dias 20/10 e 10/11. \n Considera-se cumprido este acordo após a quitação integral do valor pendente acima referido, relativo ao contrato de prestação de serviço educacional estabelecido entre as partes. O presente acordo constitui título executivo extrajudicial, podendo ser executado judicialmente. \n Camila Ilges dos Santos– Medianda \n Fulano Costa - Diretor Presidente \n Fulana de Tal - Conciliadora/Mediadora""
    args:
        None
    """
    return jsonify({"status": "OK"}), 200

def send_signature_instructions(name, **kwargs):
    f"""Realizar assinatura digital por meio de plataformas como Docusign não é algo trivial para muitas pessoas que tem um pouco mais de dificuldade de mexer com aparelhos eletrônicos. Portanto, caso {name} tenha dúvidas sobre como fazer a assinatura digital, a ferramenta envia as instruções para fazer a assinatura digital por meio da ferramenta WhatsApp (ou seja, o usuário não receberá as instruções por e-mail). Assuma que o usuário já recebeu o acordo para assinatura por e-mail, portanto não invoca a ferramenta que envia o acordo por email depois de enviar as instruções. Se o usuário precisar que você envie novamente o acordo, ele pedirá, e você deve ser reativo às mensagens do usuário. Por isso não invoca nenhuma outra ferramenta após, sem que seja necessário. Além disso, envia as instruções apenas uma vez.
    args:
        name: nome do usuário
    """
    
    send_message(f"Entendi, {name}. Vou te enviar instruções para realizares a assinatura digital.")
    send_message("1. Abra o seu aplicativo do email\n 2. Clique no link do Docusign\n 3. Clique em \"Assinar\" no canto superior direito\n 4. Preencha seus dados\n 5. Pronto")
    send_message("Caso continues com dúvidas me avise")

    print("Instruções enviadas com sucesso.")
    return jsonify({"status": "OK"}), 200