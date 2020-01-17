# heise-online-news-telegram-bot

This is the inofficial heise online telegram bot.

## Installation

This is how to install and run the software afterwards

### Install the requirements

``` bash
pip3 install -r requirements.txt
```

### Copy configuration

``` bash
cd /opt/scripts/heise-online-news-telegram-bot/
cp heise_online_bot/config/config.ini.example heise_online_bot/config/config.ini
cp heise_online_bot/config/news.ini.example heise_online_bot/config/news.ini
cp heise_online_bot/config/users.ini.example heise_online_bot/config/users.ini
```

### Run the bot as systemd service

Edit the configuration file:
`sudo vim /etc/systemd/system/heise-online-bot.service`

Paste this and change the paths for your installation:

``` bash
[Unit]
Description=Heise Online News Telegram Bot
Wants=network-online.target
After=syslog.target time-sync.target network.target network-online.target

[Service]
ExecStart=/usr/bin/python3 heise_online_bot/
WorkingDirectory=/opt/scripts/heise-online-news-telegram-bot/
Restart=always
RestartSec=10
StandardOutput=none
StandardError=none
SyslogIdentifier=heise-online-bot
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

Reload Daemon:
`systemctl daemon-reload`

Enable autostart of daemon:
`systemctl enable heise-online-bot`

Start daemon:
`systemctl start heise-online-bot`
