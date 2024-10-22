import requests
import json

token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQsAAAABAAUABwCA3buUBtTcSAgAgB3foknU3EgCAO03Vj2VbENBiMk4NjsFY84VAAEAAAAYAAEAAAAFAAAADQAkAAAAZGNmYTg5MjYtNjY2ZS00ZWM0LWIyNWMtY2VjODdjMjk1ODFiIgAkAAAAZGNmYTg5MjYtNjY2ZS00ZWM0LWIyNWMtY2VjODdjMjk1ODFiMAAAmY-Xu9DcSDcApxxjKibERE6xXCgMsiFQFhIAAQAAAA0AAAByZWZyZXNoX3Rva2Vu.Ton9OhB1mOZg1tkWtSl6H8ya8Z2HoyX6wCB1Lanhz45tPE4gab4hx4tHXQjnGyIDXrzyiV-N-qqBTzIAOALuWaotn8oDGcg6w4V18B4omlR_4-cuPy8fCPdv4nh0sKcnq6kC2vZvbC_iPbFa3y99SyYnfCYGbz9nKXGBgXH7fiufCtjLVAuXRD_Mto0eUMqLUM4I9YemOL_pXCXvdFtQGqCN98j3tlgFxOdUS61pcGx97eBTZDtIxpbkIeW-iM-COU3ksUJys4AZG2pp5Vru4fc19nTCtEGyw_WXuBxbI6l2o3jACehp39kliJlu1JY6NUmFNpGMNEnVL9_Fyyb_9w'

def createEnvelope(accountId):

    body = {
        "envelopeDefinition": {
            "allowComments": True
        }
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "+5551998683377",
        "type": "text",
        "text": {"preview_url": False, "body": body},
    }
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{accountId}/envelopes"

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


createEnvelope('9341e738-6d12-4a9c-b7a7-91803a049721')