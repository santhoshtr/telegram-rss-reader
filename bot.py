import logging
import time
import os

from dotenv import load_dotenv
from telegram import ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from db import (add_feed_source, get_all_sources, get_sources,
                is_already_present, remove_feed_source,
                update_source_timestamp)
from feed import format_feed_item, get_feed_info, read_feed
from archive import capture

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def add_feed(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    source = context.args[0]
    # /add https://thegradient.pub/rss
    if is_already_present(user, source):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=source + ' already exists.')
    else:
        add_feed_source(user, source)
        feed_info = get_feed_info(source)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=source + ' added.')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=feed_info)


def remove_feed(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    source = context.args[0]
    # /remove https://thegradient.pub/rss
    if is_already_present(user, source):
        remove_feed_source(user, source)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=source + ' removed.')
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=source + ' does not exist.')


def list_feeds(update: Update, context: CallbackContext) -> None:
    userId = update.effective_chat.id
    sources = get_sources(userId)
    if len(sources):
        context.bot.send_message(
            chat_id=userId, text="\n".join(sources))
    else:
        context.bot.send_message(
            chat_id=userId, text="No sources added yet")

def archive_link(update: Update, context: CallbackContext):
    user = update.effective_chat.id
    source = context.args[0]
    url, captured = capture(source)
    context.bot.send_message(chat_id=user, text=url)

def text(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    text_received = update.message.text
    context.bot.send_message(
        chat_id=user, text='To add a feed use /add feedurl')


def help(update: Update, context: CallbackContext) -> None:
    user = update.effective_chat.id
    context.bot.send_message(
        chat_id=user, text='To add a feed use /add feedurl')


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def error(update, context):
    update.message.reply_text('an error occured')
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)


def fetch_feeds(context: CallbackContext):
    sources = get_all_sources()
    filter_words = os.getenv('EXCLUDE_WORDS').splitlines()
    for source in sources:
        feeds = read_feed(source["url"], filter_words)
        logger.info(msg="Found " + str(len(feeds)) +
                    " feeds from " + source["url"])
        entry_index = 0
        last_post_updated_time= 0
        for entry in feeds:
            entry_index = entry_index+1
            if entry_index > 10:
                break
            if entry.has_key('published_parsed'):
                post_updated_time = int(time.strftime(
                    "%Y%m%d%H%M%S", entry.published_parsed))
            elif entry.has_key('updated_parsed'):
                post_updated_time = int(time.strftime(
                    "%Y%m%d%H%M%S", entry.updated_parsed))
            else:
                logger.error(msg=source["url"] + " has no time info")
                break
            last_updated_time = int(source["last_updated"])
            if post_updated_time > last_post_updated_time:
                last_post_updated_time = post_updated_time
            if post_updated_time > last_updated_time:
                context.bot.send_message(chat_id=source["userId"],
                                         text=format_feed_item(entry),
                                         parse_mode=ParseMode.HTML)
                if os.getenv('ARCHIVE_POSTS') == 'true':
                    # Add the link to archive.org
                    capture(entry.link)


        update_source_timestamp(source["userId"], source["url"], last_post_updated_time)


def main():
    load_dotenv()  # take environment variables from .env.
    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler('add', add_feed))
    dispatcher.add_handler(CommandHandler('remove', remove_feed))
    dispatcher.add_handler(CommandHandler('list', list_feeds))
    dispatcher.add_handler(CommandHandler('archive', archive_link))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    # add an handler for errors
    # dispatcher.add_error_handler(error)

    job_queue = updater.job_queue
    job_queue.run_repeating(
        fetch_feeds, interval=int(os.getenv('FEED_UPDATE_INTERVAL')), first=10)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
