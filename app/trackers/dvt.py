import re
import unicodedata
from bs4 import BeautifulSoup
import requests
from trackers.tracker import Tracker
from app.utils import check_ratio


class DVTTracker(Tracker):
    name = "DivTeam"
    abbr = "DVT"

    def __init__(self):
        super().__init__(name=self.name, abbr=self.abbr)

    def get_info(self) -> dict:
        url = "https://divteam.com/index.php?page=faq"
        response = requests.get(url, self.cookies)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch info from {self.name} tracker. Status code: {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.findAll("tr")
        min_ratio_container = [tr for tr in trs if "¿Cual es el ratio minimo?" in tr.text][0]
        min_ratio = float(min_ratio_container.find('font').text.strip().split(' ')[0])
        min_seedtime_container = [tr for tr in trs if "¿Hay Hit & Run?" in tr.text][0]
        min_seedtime = min_seedtime_container.findAll('font')[1].text.strip()
        min_seedtime = min_seedtime.split(' ')[-1]
        min_seedtime = f"Recomendable >= {min_seedtime}"
        return {
            "min_ratio": min_ratio,
            "min_seedtime": min_seedtime,
        }

    def get_data(self) -> dict:
        uuid = self.cookies["uid"]
        url = f"https://divteam.com/index.php?page=userdetails&id={uuid}"
        response = requests.get(url, cookies=self.cookies)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch data from {self.name} tracker. Status code: {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        list_group = soup.find("ul", class_="list-group")
        items = list_group.find_all('li', class_='bot-flex')[1:]
        data = {}
        for item in items:
            key = item.find("strong").text.strip()
            value = item.contents[1].strip()
            data[key] = value
        if "min_ratio" in self.info:
            operator = check_ratio(data["Ratio"], self.info["min_ratio"])
            data["Ratio"] = f"{data['Ratio']} {operator} {self.info['min_ratio']}"
        data["Min Seedtime"] = self.info["min_seedtime"]
        data['Hit and Run'] = "No tiene"
        if self._get_url_flag():
            data["URL"] = url
        return data
