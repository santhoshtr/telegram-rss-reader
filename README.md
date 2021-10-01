Telegram bot to fetch RSS feeds
===============================

This is a telegram bot that fetches RSS feeds in regular intervals and send it to you. The feed sources can be added or removed by just sending messages to the bot. Additionally, the feed URLs will be captured to archive.org.

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
ARCHIVE_POSTS=false
EXCLUDE_WORDS="കൊന്നു
കൊലപ്പെടുത്തി"
```

Make sure to edit the values as per your environment.
FEED_UPDATE_INTERVAL is in minutes. So 1800 = 30*60. That is, fetch the feeds in every 30 minutes

EXCLUDE_WORDS are words to filter the feeds. If you don't want to read posts with titles containing these words, add those words here, one per line.

ARCHIVE_POSTS controls whether posts need to be archived in archive.org or not.

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
* `/archive` to archive a given link in archive.org
