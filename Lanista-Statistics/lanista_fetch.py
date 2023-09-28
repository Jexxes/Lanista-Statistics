import requests
from bs4 import BeautifulSoup
import json

# Author Maximilian Ygdell (2023-09-29)

BASE_URL = 'https://beta.lanista.se'

class LanistaScraper:
    # Creates a session, sets header data so that the API call can be made
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Dnt": "1",
            "Referer": f"{BASE_URL}/game/avatar/me/levelhistory",
            "Sec-Ch-Ua": '"Chromium";v="116"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "LanistaOS",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        }

    # Fetches the unique and randomised token needed to validate the login
    def fetch_token(self):
        try:
            r = self.session.get(BASE_URL)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'html5lib')
            token_field = soup.find('input', attrs={'name': '_token'})
            return token_field['value'] if token_field else None
        except requests.RequestException as e:
            print(f"Ett fel uppstod vid inhämtning av token {e}")
            return None
    
    def get_gladiator_info(self):
        gladiator_url = f"{BASE_URL}/api/users/me"
        gladiator_info = self.fetch_data(gladiator_url)
        return gladiator_info

    # Logs the user in using a payload and information given from the GUI
    def login(self, email, password):
        token = self.fetch_token()
        if token is None:
            return None

        login_payload = {"_token": token, "email": email, "password": password}
        response = self.session.post(f"{BASE_URL}/login", data=login_payload)
        return response.status_code

    # Returns the response json if statistics was successfully gathered
    def fetch_data(self, url):
        response = self.session.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        return response.json()