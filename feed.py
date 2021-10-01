import feedparser
from urllib.error import URLError

def read_feed(source, filter_words):
    try:
        feed = feedparser.parse(source)
        entries = feed.entries
        return [entry for entry in entries if
              all(filter_word not in entry.get("title","") for filter_word in filter_words)]
    except URLError:
        return []


def format_feed_item(post):
    return "<a href='"+ post.get("link", "link?")+ "'>" + post.get("title", "title?") + "</a>"


def get_feed_info(source):
    try:
        feed = feedparser.parse(source)
        return feed['channel']['title'] + "\n" + feed['channel']['link']
    except URLError:
        return 'Could not connect to '+ source
