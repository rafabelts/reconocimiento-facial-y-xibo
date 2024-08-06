import requests
import os
from dotenv import load_dotenv


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

def reloadContent(displayId):
    cms_url = 'https://icsicorp.xibo.cloud/api'

    access_token = getToken()
    display_id=displayId
    command_url =  f'{cms_url}/displaygroup/{display_id}/action/command'
    command = 'SCHEDULE_NOW'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json' 
    }

    data = {
        'command': command,
        'params': {
            'command': 'restart'
        }
    }

    response = requests.post(command_url, headers=headers, json=data)

    if response.status_code == 200:
        print('Reiniciado')
    else:
        print('Error al reiniciar: ', response.json())