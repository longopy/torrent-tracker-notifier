import abc
import json
import os

import apprise


class Tracker(abc.ABC):
    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr
        self.username = self._get_username()
        self.cookies = self._get_cookies()
        self.info = self.get_info()

    def _get_username(self):
        username = os.environ.get("USERNAME")
        return os.environ.get(f"{self.abbr}_USERNAME", username)
    
    def _get_cookies(self):
        if not os.path.exists(f'cookies/{self.abbr.lower()}.json'):
            raise FileNotFoundError(f"File cookies/{self.abbr.lower()}.json not found")
        with open(f'cookies/{self.abbr.lower()}.json', 'r') as f:
            cookies = json.load(f)
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        return cookies_dict
    
    def _get_url_flag(self):
        return os.environ.get(f"SEND_URL", True)
    
    def get_info(self) -> dict:
        return None
        
    def get_data(self) -> dict:
        return None
    
    def _get_notify(self):
        notify = os.environ.get("NOTIFY")
        return os.environ.get(f"{self.abbr}_NOTIFY", notify)

    def _send_data(self, data: dict):
        app = apprise.Apprise()
        notifications = self._get_notify().split(',')
        if not notifications:
            raise ValueError("No notifications set")
        for notification in notifications:
            app.add(notification)
        msg = f"[Tracker: {self.name} ({self.abbr})]\n"
        for key, value in data.items():
            msg += key + ": " + value + "\n"
        title = os.environ.get('NOTIFY_TITLE', 'Torrent Tracker Notifier')
        app.notify(title=title, body=msg)

    def process(self):
        try:
            data = self.get_data()
        except Exception as e:
            data = {"error": str(e)}
        if data:
            self._send_data(data)