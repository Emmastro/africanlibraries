import json
import requests

api_token = 'token' # TODO: get token from env variables
api_url_base = 'https://www.googleapis.com/books/v1/'

def get_book_details(search):

    api_url = '{base}volumes?q={search}&key={token}'.format(base=api_url_base, search=search, token=api_token)

    response = requests.get(api_url)#, headers=headers)
    if response.status_code == 200:
        #content = json.loads(response.content.decode('utf-8'))
        
        #book_info = content.get('volumeInfo')
        
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
