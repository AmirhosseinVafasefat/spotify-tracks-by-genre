import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class SpotifyAuthManager:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = None
        self.token_expires_at = 0

    def _request_token(self):
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        headers = {
            "Authorization": f"Basic {self._encode_credentials()}"
        }

        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

        result = response.json()
        self.token = result["access_token"]
        self.token_expires_at = time.time() + result["expires_in"] - 10  # renew a few seconds early

    def _encode_credentials(self):
        import base64
        raw = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(raw.encode()).decode()

    def get_token(self) -> str:
        if self.token is None or time.time() >= self.token_expires_at:
            self._request_token()
        return self.token

    def refresh_token(self) -> None:
        self._request_token()

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.get_token()}"
        }
