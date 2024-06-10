import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

class CoinMarketCap:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com"
        self.driver = self._setup_driver()

    def _setup_driver(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        return driver

    def _make_request(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def _scrape_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        data['name'] = soup.find('h1', class_='cmc-details-panel-name').text.strip()
        data['symbol'] = soup.find('small', class_='cmc-symbol').text.strip()
        data['price'] = soup.find('div', class_='cmc-details-panel-price').text.strip()
        data['market_cap'] = soup.find('div', class_='cmc-details-panel-market-cap').text.strip()
        data['official_links'] = [a['href'] for a in soup.find_all('a', class_='cmc-link')]
        data['social_links'] = [a['href'] for a in soup.find_all('a', class_='cmc-social-link')]
        return data

    def scrape_coin_data(self, coin_symbol):
        url = f"{self.base_url}/currencies/{coin_symbol.lower()}/"
        html = self._make_request(url)
        data = self._scrape_data(html)
        return data