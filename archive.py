import savepagenow

USERAGENT="github.com/santhoshtr/telegram-rss-reader"

def capture(url):
    try:
        return savepagenow.capture_or_cache(url, user_agent=USERAGENT)
    except Exception:
        pass