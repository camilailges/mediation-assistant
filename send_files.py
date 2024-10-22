import base64
import requests
import logging
import json
from dotenv import load_dotenv
import os
from flask import Blueprint, request, jsonify, current_app

from llm_service import generate_response, process_text_for_whatsapp
from security import signature_required

webhook_blueprint = Blueprint("webhook", __name__)

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# Função que recebe arquivos de uma mensagem
def upload_file(message):

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