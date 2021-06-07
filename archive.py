import savepagenow

USERAGENT="github.com/santhoshtr/telegram-rss-reader"

def capture(url):
    return savepagenow.capture_or_cache(url,  user_agent=USERAGENT)