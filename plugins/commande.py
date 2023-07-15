import logging
import os
import re
import time
from Script import script
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


def get_username(url):
    match = re.search(proregpat, url)
    if match:
        return match.group(2)


def create_caption(user):
    return f"Username: {user.username}\nFull Name: {user.full_name}\nFollowers: {user.followers}\nFollowing: {user.followees}"


from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command(["start"]))
def start(client, message):
    name = message.from_user.username
    
    button1 = InlineKeyboardButton("Channel", url="https://t.me/HTechMedia")
    button2 = InlineKeyboardButton("Support", url="https://t.me/HTechMediaSupport")
    button3 = InlineKeyboardButton("Source", url="https://github.com/Nxt-Stark/Instagram-dp-downloader")
    button4 = InlineKeyboardButton("Owner", url="https://t.me/NxtStark")
    button5 = InlineKeyboardButton("Help", url="https://www.youtube.com/c/HTechMedia")

    keyboard = InlineKeyboardMarkup([[button1, button2], [button3, button4],[button5]])

    message.reply_photo(
        photo="https://telegra.ph/file/85a40fa28ea0f0d4db1c6.jpg"
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME), 
        reply_markup=keyboard
        parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command(["help"]))
def help_msg(client, message):
    button1 = InlineKeyboardButton("Devoloper", url="https://t.me/NxtStark")
    button2 = InlineKeyboardButton("Support", url="https://t.me/HTechMediaSupport")
    button3 = InlineKeyboardButton("Youtube", url="https://www.youtube.com/c/HTechMedia")
    keyboard = InlineKeyboardMarkup([[button1, button2], [button3]])
    message.reply_video(
        video="https://example.com/video.mp4"
        caption=script.HELP_TXT,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML)



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



