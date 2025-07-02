import os
from dotenv import load_dotenv
import base64
from requests import post
import json

def get_token():
    #Loading .env file and extracting client ID and client secret
    load_dotenv()
    client_id: str = os.getenv("CLIENT_ID")
    client_secret: str = os.environ.get("CLIENT_SECRET")
    
    #Preparting client ID and client secret to be sent in the right format(base 64)
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_auth_header(token):
    #Create a header from the token
    return {"Authorization":"Bearer " + token}