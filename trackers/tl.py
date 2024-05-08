
import re
from bs4 import BeautifulSoup
import requests
from trackers.tracker import Tracker
from utils import check_ratio


class TLTracker(Tracker):
    name = 'TorrentLeech'
    abbr = 'TL'
    
    def __init__(self):
        super().__init__(name=self.name, abbr=self.abbr)
    
    def get_info(self) -> dict:
        url = "http://wiki.torrentleech.org/doku.php/hnr"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch info from {self.name} tracker. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_general_info = soup.find('h1', class_='sectionedit2')
        min_ratio_div = h1_general_info.find_next_sibling().find('div', class_='li', string=re.compile("ratio")).text
        min_ratio = int(min_ratio_div.split(':')[-1].split(' ')[0].strip())

        h1_seedtime = soup.find('h1', class_='sectionedit3')
        min_seedtime_div = h1_seedtime.find_next_sibling().find('table', class_='inline')
        min_seedtime_by_user_class = {}
        for row in min_seedtime_div.findAll('tr'):
            aux = row.findAll('td')
            if aux:
                min_seedtime_by_user_class[aux[0].string] = aux[1].string
        return {'min_ratio': min_ratio, 'min_seedtime_by_user_class': min_seedtime_by_user_class}

    def get_data(self) -> dict:
        url = f"https://www.torrentleech.org/profile/{self.username}/view"
        response = requests.get(url, cookies=self.cookies)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {self.name} tracker. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        sub_navbar = soup.find('div', class_='sub-navbar')
        center_top_bar = sub_navbar.find_all('span', class_='centerTopBar')[1]
        menu_info_list = center_top_bar.find_all('span', class_='menu-info')
        items = menu_info_list[0].findAll('div', class_='div-menu-item')
        user_class = soup.find('div', class_='label-user-class').text.strip()
        data = {"User Class": user_class}
        # first line
        for item in items:
            if item.attrs['title']:
                key = item.attrs['title'].strip()
            else:
                key = 'Notifications'
            value = item.text.strip()
            data[key] = value
        # second line
        items = menu_info_list[1].findAll('div', class_='div-menu-item')
        for item in items:
            info = item.text.split(':')
            key = info[0].strip()
            value = info[1].strip()
            data[key] = value

        if 'Ratio' not in data:
            raise ValueError(f"Failed to fetch data from {self.name} tracker. Ratio not found")
        if 'Achievements' in data:
            data['Achievements'] = data['Achievements'].replace('new', '').strip()
        if 'min_ratio' in self.info:
            operator = check_ratio(data['Ratio'], self.info['min_ratio'])
            data['Ratio'] = f"{data['Ratio']} {operator} {self.info['min_ratio']}"
        data['Min Seedtime'] = self.info['min_seedtime_by_user_class'][user_class]
        if self._get_url_flag():
            data["URL"] = url
        return data
    
