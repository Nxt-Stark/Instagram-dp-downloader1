import logging
import os
import re
import time
from traceback import format_exc
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from instaloader import Instaloader, Profile


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


L = Instaloader()
TOKEN = os.getenv("BOT_TOKEN")
APP_NAME = os.getenv("APP_NAME")
TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME")

mediaregpat = r"(https?:\/\/(?:www\.)?instagram\.com\/(?:p|reel|tv)\/([^\/?#&\n]+)).*"
proregpat = r"(https?:\/\/(?:www\.)?instagram\.com\/([a-z1-9_\.?=]+)).*"


def welcome_msg():
    return "Welcome to the Instagram DP Saver Bot!"


def get_username(url):
    match = re.search(proregpat, url)
    if match:
        return match.group(2)


def create_caption(user):
    return f"Username: {user.username}\nFull Name: {user.full_name}\nFollowers: {user.followers}\nFollowing: {user.followees}"


@Client.on_message(filters.command(["start"]))
def start(client, message):
    name = message.from_user.username
    message.reply_text(welcome_msg())


@Client.on_message(filters.command(["help"]))
def help_msg(client, message):
    message.reply_text("Send any Instagram user's username (without @) or their profile URL to get their profile picture.")


@Client.on_message(filters.command(["contact"]))
def contact(client, message):
    keyboard = [[InlineKeyboardButton(
        "Contact", url=f"telegram.me/{TELEGRAM_USERNAME}")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message.reply_text('Contact the Maker:', reply_markup=reply_markup)


@Client.on_message(filters.text)
def username(client, message):
    query = message.text

    if not re.compile(mediaregpat).search(query):
        msg = message.reply_text("Downloading...")
        if re.compile(proregpat).search(query):
            query = get_username(query)
        chat_id = message.chat.id
        try:
            user = Profile.from_username(L.context, query)
            caption_msg = create_caption(user)
            client.send_photo(
                chat_id=chat_id,
                photo=user.profile_pic_url,
                caption=caption_msg,
                parse_mode='markdown'
            )
            message.reply_text("Can you support me by rating this bot 😃", reply_markup=InlineKeyboardMarkup(ratingkey))
            msg.edit_text("Finished.")
            time.sleep(5)
        except Exception as e:
            print(format_exc())
            msg.edit_text("Try again 😕😕 Check the username correctly")
    else:
        message.reply_html("This bot only supports downloading of profile pictures. Please do not send media URLs.")


@Client.on_message(filters.command(["source"]))
def source(client, message):
    message.reply_text("You can get the source code of this bot here:\n\nhttps://github.com/anishgowda21/Instagram_DP_Saver_Bot")


@Client.on_message(filters.private)
def error(client, message):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', message, message.text)


def main():
    app = Client("my_bot", bot_token=TOKEN)
    app.run()


if __name__ == '__main__':
    main()
