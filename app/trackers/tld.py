
import re
from bs4 import BeautifulSoup
import requests
from trackers.tracker import Tracker
from app.utils import check_ratio


class TLDTracker(Tracker):
    name = 'TorrentLand'
    abbr = 'TLD'
    
    def __init__(self):
        super().__init__(name=self.name, abbr=self.abbr)
    
    def get_info(self) -> dict:
        return {'min_ratio': 0.4, 'min_seedtime': '96hours'}

    def get_data(self) -> dict:
        url = f"https://torrentland.li/users/{self.username}"
        response = requests.get(url, cookies=self.cookies)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {self.name} tracker. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        user_class = soup.find('span', class_='badge-user').text.strip()
        data = {"User Class": user_class}
        table = soup.find('table', class_='user-info')
        items = table.findAll('tr')[4:11]
        for item in items:
            tds = item.findAll('td')
            key = tds[0].text.strip()
            value = tds[1].text.strip()
            if key in ('Descarga total', 'Subida total'):
                value = value.split(' ')[0]
            data[key] = value
        if 'Ratio' not in data:
            raise ValueError(f"Failed to fetch data from {self.name} tracker. Ratio not found")
        if 'min_ratio' in self.info:
            operator = check_ratio(data['Ratio'], self.info['min_ratio'])
            data['Ratio'] = f"{data['Ratio']} {operator} {self.info['min_ratio']}"
        if 'min_seedtime' in self.info:
            data['Min Seedtime'] = self.info['min_seedtime']
        if self._get_url_flag():
            data["URL"] = url
        return data
    
