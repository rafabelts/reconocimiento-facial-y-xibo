import requests
import os
from dotenv import load_dotenv
from requests.sessions import preferred_clock


load_dotenv()
def getToken():
    load_dotenv()
    cms_url = 'https://icsicorp.xibo.cloud/api'
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    # url para obtener el token de autorizacion
    token_url = f'{cms_url}/authorize/access_token'

    # Solicitar el token
    response = requests.post(
        token_url, data={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
    })
  
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return 'Error'



def reloadContent(display_group_id):
    access_token = getToken()
    cms_url = 'https://icsicorp.xibo.cloud/api'
    webhook_url = f"{cms_url}/displaygroup/{display_group_id}/action/triggerWebhook"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "triggerCode": "copilot" 
    }
    
    response = requests.post(webhook_url, headers=headers, json=payload)

    if response.status_code == 204:
        return "Reloaded"
    else:
        return "Failed"
