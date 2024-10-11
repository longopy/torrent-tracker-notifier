<p align="center">
  <img src="https://raw.githubusercontent.com/longopy/torrent-tracker-notifier/master/logo.png" alt="Torrent Tracker Notifier logo" width="100" height="100">
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
| NOTIFY          |                          | Notification services to use (Telegram, Pushover, Slack, ...). You can generate the syntax by following the guide from [apprise](https://github.com/caronc/apprise). You can also define a different environment variable for each tracker by using its abbreviation: FNP_NOTIFY, TL_NOTIFY, etc.  |
| USERNAME        |                          | You must indicate the user you will use to get the information from the trackers. You can also define a different environment variable for each tracker by using its abbreviation: FNP_USERNAME, TL_USERNAME, etc.                                                |
| TRACKERS        |                          | To indicate the trackers you want to use. List of abbreviations in lowercase comma-separated. e.g FNP,TL,TLD,DVT,HDO                                                |
| SEND_URL        | true                     | If you want to include a link to the tracker in the notification.                                                                                                   |
| CRON_EXPRESSION |                          | Cron expression indicating the periocity of the execution. You can generate it using the service: [crontab.guru](https://crontab.guru/).                            |
| TZ              |                          | Defines the time zone in which the cron will work. You can see the options available here: [Timezones](https://docs.diladele.com/docker/timezones.html).            |

## How to use

1. Create a file called `docker-compose.yml` in a folder, and set the environment variables.
```
services:
  tracker-notifier:
    image: ghcr.io/longopy/torrent-tracker-notifier:latest
    container_name: tracker-notifier
    environment:
      - NOTIFY_TITLE=Torrent Tracker Notifier
      - NOTIFY=tgram://<BOT_TOKEN>/<CHAT_ID>
      - USERNAME=<USERNAME>
      - TRACKERS=FNP,TL,TLD,DVT,HDO
      - SEND_URL=true
      - CRON_EXPRESSION=0 12 */2 * *
      - TZ=Europe/Madrid
    volumes:
        - ./cookies:/opt/app/cookies
```
2. Create a folder named `cookies` in the root folder and add a `.json` file for each tracker you want to use. The file name should be the abbreviation of the tracker in lower case. For example, `fnp.json`, `tl.json`, `tld.json`, `dvt.json`, `hdo.json`.
   If the tracker was specified in the `TRACKERS` environment variable, it should have an associated cookie file in this folder.
   > You can extract the cookies using browser extensions like `EditThisCookie`: [Chrome](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) or [Firefox](https://addons.mozilla.org/es/firefox/addon/edithiscookie/)
3. Execute the container using docker-compose:

```bash
docker-compose up -d
```

Also you can use the environment variables from an file `.env`, modifying the docker-compose.yml:
```
services:
  tracker-notifier:
    image: ghcr.io/longopy/torrent-tracker-notifier:latest
    container_name: tracker-notifier
    volumes:
        - ./cookies:/opt/app/cookies
    env_file: ./.env
```

## Collaborators

Special thanks to all the developers who have contributed to Torrent Tracker Notifier

<table id='collaborators'>
<tr align='center'>
    <td id='acallejp97'>
        <a href='https://github.com/acallejp97'>
            <img src='https://github.com/acallejp97.png' width='92px;' style='border-radius: 99999px;'>
        </a>
        <br>
        <a href='https://github.com/acallejp97'>acallejp97</a>
    </td>
     <td id='longopy'>
        <a href='https://github.com/longopy'>
            <img src='https://github.com/longopy.png' width='92px;' style='border-radius: 99999px;'>
        </a>
        <br>
        <a href='https://github.com/longopy'>longopy</a>
    </td>
    </tr>
</table>
