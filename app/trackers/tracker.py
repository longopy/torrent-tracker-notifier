import abc
import json
import os

import apprise
import requests
from bs4 import BeautifulSoup


class Tracker(abc.ABC):
    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr
        self.username = self._get_username()
        self.cookies = self._get_cookies()
        self.info = self.get_info()
        self.show_downloads = self.get_download_flag()

    @staticmethod
    def get_download_flag():
        return os.environ.get(f"INCLUDE_DOWNLOADING_LIST", "false").lower() == "true"

    def _get_username(self):
        username = os.environ.get("USERNAME")
        return os.environ.get(f"{self.abbr}_USERNAME", username)

    def _get_cookies(self):
        if not os.path.exists(f"cookies/{self.abbr.lower()}.json"):
            raise FileNotFoundError(f"File cookies/{self.abbr.lower()}.json not found")
        with open(f"cookies/{self.abbr.lower()}.json", "r") as f:
            cookies = json.load(f)
        cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
        return cookies_dict

    def _get_url_flag(self):
        return os.environ.get(f"SEND_URL", True)

    def get_info(self) -> dict:
        return None

    def get_data(self) -> dict:
        return None

    def _get_notify(self):
        notify = os.environ.get("NOTIFY")
        notify = os.environ.get(f"{self.abbr}_NOTIFY", notify)
        if not notify:
            return ""
        return notify

    def _send_data(self, data: dict):
        notify_string = self._get_notify()
        if not notify_string:
            # No notifications configured, print to log instead
            msg = f"[Tracker: {self.name} ({self.abbr})]\n"
            for key, value in data.items():
                msg += key + ": " + value + "\n"
            print(msg)
            return

        app = apprise.Apprise()
        notifications = notify_string.split(",")
        # Filter out empty strings that might result from splitting
        notifications = [n.strip() for n in notifications if n.strip()]
        if not notifications:
            # No valid notifications configured, print to log instead
            msg = f"[Tracker: {self.name} ({self.abbr})]\n"
            for key, value in data.items():
                msg += key + ": " + value + "\n"
            print(msg)
            return

        for notification in notifications:
            app.add(notification)
        msg = f"[Tracker: {self.name} ({self.abbr})]\n"
        for key, value in data.items():
            msg += key + ": " + value + "\n"
        title = os.environ.get("NOTIFY_TITLE", "Torrent Tracker Notifier")
        app.notify(title=title, body=msg)

    def process(self):
        try:
            data = self.get_data()
        except Exception as e:
            data = {"error": str(e)}
        if data:
            self._send_data(data)

    def get_associated_torrent_list(self, url) -> str:
        response = requests.get(url, cookies=self.cookies)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to fetch downloading list from {self.name} tracker. Status code: {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tbody")
        rows = table.findAll("tr")
        downloading_list = ""
        for row in rows:
            texts = row.findAll("a")
            name = texts[0].text.strip()
            name = name.split(")")[0].strip()
            downloading_list += f"\n- {name})"
        return downloading_list
