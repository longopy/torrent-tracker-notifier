<p align="center">
  <img src="https://i.ibb.co/QrDtVss/OIG1-removebg-preview.png" alt="Torrent Tracker Notifier logo" width="100" height="100">
  <h1 align="center"> Torrent Tracker Notifier </h1>
  </p>

Obtains information from your trackers on a regular basis.

## Supported trackers

- [Feer no peer](https://fearnopeer.com/) (FNP)
- [TorrentLeech](https://www.torrentleech.org) (TL)
- [TorrentLand](https://torrentland.li/) (TLD)
- [DivTeam](https://divteam.com/) (DVT)
- [HD-Olimpo](https://hd-olimpo.club/) (HDO)

## Environment Variables

| Option          | Default                  | Description                                                                                                                                                         |
| --------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NOTIFY_TITLE    | Torrent Tracker Notifier | Optional title for notifications, e.g. for Telegram, Pushover, etc                                                                                                  |
| NOTIFY          |                          | Notification services to use (Telegram, Pushover, Slack, ...). You can generate the syntax by following the guide from [apprise](https://github.com/caronc/apprise) |
| TRACKERS        |                          | To indicate the trackers you want to use. List of abbreviations in lowercase comma-separated. e.g FNP,TL,TLD,DVT,HDO                                                |
| SEND_URL        | true                     | If you want to include a link to the tracker in the notification.                                                                                                   |
| CRON_EXPRESSION |                          | Cron expression indicating the periocity of the execution. You can generate it using the service: [crontab.guru](https://crontab.guru/).                            |
| TZ              |                          | Defines the time zone in which the cron will work. You can see the options available here: [Timezones](https://docs.diladele.com/docker/timezones.html).            |

## How to use

1. Create a `.env` file with the environment variables in the root folder. You must set the environment variables listed above. You can use the file `.env.example` as a template.
2. Create a folder named `cookies` in the root folder and add a `.json` file for each tracker you want to use. The file name should be the abbreviation of the tracker in lower case. For example, `fnp.json`, `tl.json`, `tld.json`, `dvt.json`, `hdo.json`.
   If the tracker was specified in the `TRACKERS` environment variable, it should have an associated cookie file in this folder.
   > You can extract the cookies using browser extensions like `EditThisCookie`: [Chrome](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) or [Firefox](https://addons.mozilla.org/es/firefox/addon/edithiscookie/)
3. Execute the container using docker-compose:

```bash
docker-compose up -d
```
