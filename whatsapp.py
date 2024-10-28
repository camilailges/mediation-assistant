import asyncio
import base64
from queue import Queue
from threading import Thread
import time
import requests
import logging
import json
from dotenv import load_dotenv
import os
from flask import Blueprint, request, jsonify, current_app

from llm_service import generate_response, process_text_for_whatsapp
from security import signature_required

webhook_blueprint = Blueprint("webhook", __name__)
# from .decorators.security import signature_required

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

message_queue = Queue()

def queue_worker(app):
    # current_app.app_context().push()
    app.app_context().push()
    # with current_app.test_request_context():
    # with current_app.app_context():
    while True:
        if message_queue.empty():
            print("Fila vazia. Aguardando novas mensagens...")
        message = message_queue.get() # Pega a próxima mensagem da fila
        logging.info(f"Received message: {message}")
        if message is None:
            print("is None")
            break
        with current_app.app_context():
            handle_message(message)
        message_queue.task_done()

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

message = "Olá! Eu sou o Assistente do Grupo Mediar."
send_message(message)
send_message("Eu posso lhe ajudar com questões como: tirar dúvidas gerais sobre acordo assinado, enviar informações do pagamento e ajudar com a realização da assinatura digital.")
# send_message_file()
# send_message("Você tem alguma dúvida a respeito do documento assinado? Estou aqui para ajudar com qualquer questão que tenhas sobre ele. Você tem alguma dúvida ou preocupação?")

def process_whatsapp_message(body):

    # Filtrar mensagens por timestamp maior que a hora atual - 12 minutos (0.2 horas)
    if "messages" in body["entry"][0]["changes"][0]["value"]:
        current_time = time.time()
        body["entry"][0]["changes"][0]["value"]["messages"] = [
            message for message in body["entry"][0]["changes"][0]["value"]["messages"]
            if int(message["timestamp"]) > (current_time - 1000 * 60 * 60 * 0.2) / 1000
        ]

    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    response = generate_response(message_body, name)
    response = process_text_for_whatsapp(response)

    print("response: "+response)

    send_message(response)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )

def handle_message(message):
    print("handle_message")
    # body = request.get_json()
    body = message

    if (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("statuses")
    ):
        logging.info("Received a WhatsApp status update.")
        return jsonify({"status": "ok"}), 200

    try:
        if is_valid_whatsapp_message(body):
            process_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), 400

# Required webhook verifictaion for WhatsApp
def verify():
    print("verify")
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == current_app.config["VERIFY_TOKEN"]:
            # Respond with 200 OK and challenge token from the request
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400



def send_file():
    print("send_file entrou")
    docPath = 'acordo.pdf'
    fn = "anyname.pdf"
    caption = "You will find it useful"  # caption is optional; can be None

    # Encode the document in base64 format
    doc_base64 = None
    with open(docPath, 'rb') as doc:
        doc_base64 = base64.b64encode(doc.read())

    # doc_base64_str = doc_base64.decode('utf-8')
    # print("Documento em base64:", doc_base64_str)    

    url = 'https://khrh82bd-8000.brs.devtunnels.ms/v1/media'
    # url = 'http://127.0.0.1:8000/v1/media'

    headers = {
        "Content-type": "application/pdf",
        "Authorization": "Bearer " + ACCESS_TOKEN,
    }

    response = requests.post(url, data=doc_base64, headers=headers)
    if response.status_code == 200:
        print('Upload bem-sucedido:', response.json())
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print('Erro ao enviar o arquivo:', response.status_code, response.text)
        print(response.status_code)
        print(response.text)
        return response

@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    return verify()

# @signature_required
@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook_post():

    if is_valid_whatsapp_message(request.get_json()):
        # print("é valid")
        message_queue.put(request.get_json())
        return jsonify({"status": "received"}), 200

    return handle_message(request.get_json())
