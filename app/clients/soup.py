from bs4 import BeautifulSoup
import requests

class SoupClient:
    def __init__(self, **kwargs):
        self.base_url = kwargs.get("base_url")
        self.session = requests.Session()
    def make_soup(self, **kwargs):
        data = kwargs.get("json_data")
        html = data["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")
        return soup
    async def get_soup(self, **kwargs):
        url = f"{self.base_url}{kwargs.get("endpoint")}"
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

