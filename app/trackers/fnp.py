
import re
from bs4 import BeautifulSoup
import requests
from trackers.tracker import Tracker
from app.utils import check_ratio


class FNPTracker(Tracker):
    name = 'Feer No Peer'
    abbr = 'FNP'
    
    def __init__(self):
        super().__init__(name=self.name, abbr=self.abbr)
    
    def get_info(self) -> dict:
        url = "https://fearnopeer.com/pages/2"
        response = requests.get(url, cookies=self.cookies)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch info from {self.name} tracker. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraph = soup.find('p', string=re.compile("What is the minimum ratio required?"))
        min_ratio = paragraph.find_next('ul').text.replace('\n', '').strip()
        return {'min_ratio': min_ratio}

    def get_data(self) -> dict:
        url = f"https://fearnopeer.com/users/{self.username}"
        response = requests.get(url, cookies=self.cookies)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {self.name} tracker. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        sections = soup.find_all('section', class_='panelV2')
        traffic_section = next(section for section in sections if 'Traffic Statistics' in section.h2.text)
        data = {}
        for dt, dd in zip(traffic_section.find_all('dt'), traffic_section.find_all('dd')):
            key = dt.text.replace('\n', '').strip()
            key =  re.sub(r'\s+', ' ', key)
            value = dd.text.replace('\n', '').strip()
            value = re.sub(r'\s+', ' ', value)
            data[key] = value
        if 'Ratio' not in data:
            raise ValueError(f"Failed to fetch data from {self.name} tracker. Ratio not found")
        if 'min_ratio' in self.info:
            operator = check_ratio(data['Ratio'], self.info['min_ratio'])
            data['Ratio'] = f"{data['Ratio']} {operator} {self.info['min_ratio']}"
        data['Hit and Run'] = "There is no HnR system on this tracker."
        if self._get_url_flag():
            data["URL"] = url
        return data