Telegram bot to fetch RSS feeds
===============================

This is a telegram bot that fetches RSS feeds in regular intervals and send it to you. The feed sources can be added or removed by just sending messages to the bot.

Bot setup
=========

Create a bot account with telegram
-----------------------------------

Use the @botfather bot of telegram. Refer its [documentation](https://core.telegram.org/bots).

Create an sqlite database with the following script
------------------------------------------------

```sql
CREATE TABLE IF NOT EXISTS "sources" (
	"userid"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"last_updated"	INTEGER NOT NULL,
	PRIMARY KEY("url","userid")
);
```

Create an .env file with the following content
---------------------------------------------

```
TELEGRAM_BOT_TOKEN=XXXXXXXXXXX
FEED_DATABASE=reader.db
FEED_UPDATE_INTERVAL=1800
```

Make sure to edit the values as per your environment.
FEED_UPDATE_INTERVAL is in minutes. So 1800 = 30*60. That is, fetch the feeds in every 30 minutes

Install requirements
---------------------

```bash
pip install -r requirements.txt
```

Start the bot
-------------

```bash
python bot.py
```

Bot commands
============

* `/add feedurl` to add a new RSS/Atom feed.
* `/remove feedurl` to remove an RSS/Atom feed subscription.
* `/list` to list alll subscribed feeds.
* `/help` to get the help

