import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://beta.lanista.se'


class LanistaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,en-SE;q=0.6",
            "Dnt": "1",
            "Referer": f"{BASE_URL}/game/avatar/me/levelhistory",
            "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "macOS",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.3",
            "X-Requested-With": "XMLHttpRequest",
        }

    def fetch_token(self):
        try:
            r = self.session.get(self.BASE_URL)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'html5lib')
            token_field = soup.find('input', attrs={'name': '_token'})
            return token_field['value'] if token_field else None
        except requests.RequestException as e:
            print(f"An error occurred while fetching token: {e}")
            return None

    def login(self, email, password):
        token = self.fetch_token()
        if token is None:
            return None

        login_payload = {"_token": token, "email": email, "password": password}
        response = self.session.post(f"{BASE_URL}/login", data=login_payload)
        return response.status_code

    def fetch_data(self, url):
        response = self.session.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        return response.json()

    def save_data_to_json(self, data, filename='Lanista_leveling_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    scraper = LanistaScraper()
    api_url = f"{BASE_URL}/api/avatars/3255/levelhistory"

    data = scraper.fetch_data(api_url)
    if data:
        scraper.save_data_to_json(data)
        print("Successfully fetched and saved data.")
    else:
        print("Failed to fetch or parse data.")
