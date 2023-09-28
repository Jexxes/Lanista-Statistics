import requests
from bs4 import BeautifulSoup
import json


class LanistaScraper:
    def __init__(self):
        self.session = requests.Session()

    def fetch_token(self):
        url = 'https://beta.lanista.se'
        r = self.session.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        token_field = soup.find('input', attrs={'name': '_token'})
        if token_field is not None:
            return token_field['value']
        else:
            print("Could not find the _token field.")
            return None

    def login(self, email, password):
        token = self.fetch_token()
        if token is None:
            print("Failed to fetch the CSRF token. Cannot proceed with login.")
            return None

        login_url = "https://beta.lanista.se/login"
        payload = {
            "_token": token,
            "email": email,
            "password": password
        }
        response = self.session.post(login_url, data=payload)

        # Debugging lines, uncomment to print debugging info
        #print("=== Login Debugging ===")
        #print("Headers:", response.headers)
        #print("Cookies:", self.session.cookies.get_dict())
        #print("History:", response.history)
        #print("Redirected URL:", response.url)
        #print("========================")

        return response.status_code

    def fetch_data(self, url):
        response = self.session.get(url)

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,en-SE;q=0.6",
            "Dnt": "1",
            "Referer": "https://beta.lanista.se/game/avatar/me/levelhistory",
            "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "macOS",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.3",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = self.session.get(url, headers=headers)
        data = response.json()

        with open('Lanista_leveling_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return response.json()



if __name__ == "__main__":
    scraper = LanistaScraper()
    login_url = "https://beta.lanista.se/login"
    api_url = "https://beta.lanista.se/api/avatars/3255/levelhistory"

    data = scraper.fetch_data(api_url)
    if data:
        print("Successfully fetched data.")
        print(data)
    else:
        print("Failed to fetch or parse data.")
