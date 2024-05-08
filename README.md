# Torrent Tracker Notifier
Obtains information from your trackers on a regular basis.

## Supported trackers
- [Feer no peer](https://fearnopeer.com/) (FNP)
- [TorrentLeech](https://www.torrentleech.org) (TL)
- [TorrentLand](https://torrentland.li/) (TLD)
- [DivTeam](https://divteam.com/) (DVT)
- [HD-Olimpo](https://hd-olimpo.club/) (HDO)

## Environment Variables
| Option          	| Default                  	| Description                                                                                                                                                         	|
|-----------------	|--------------------------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| NOTIFY_TITLE    	| Torrent Tracker Notifier 	| Optional title for notifications, e.g. for Telegram, Pushover, etc                                                                                                  	|
| NOTIFY          	|                          	| Notification services to use (Telegram, Pushover, Slack, ...). You can generate the syntax by following the guide from [apprise](https://github.com/caronc/apprise) 	|
| TRACKERS        	|                          	| To indicate the trackers you want to use. List of abbreviations in lowercase separated by commas. e.g FNP,TL,TLD,DVT,HDO                                                      	|
| SEND_URL        	| true                     	| If you want to include a link to the tracker in the notification.                                                                                                   	|
| CRON_EXPRESSION 	|                          	| Cron expression indicating the periocity of the execution. You can generate it using the [crontab.guru](https://crontab.guru/) service.                             	|