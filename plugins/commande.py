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
        chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
            )
        else:
            logging.info(f"#NewUser :- Name : {message.from_user.first_name} ID : {message.from_user.id}")
    name = message.from_user.username
    
    button1 = InlineKeyboardButton("Channel", url="https://t.me/HTechMedia")
    button2 = InlineKeyboardButton("Support", url="https://t.me/HTechMediaSupport")
    button3 = InlineKeyboardButton("Source", url="https://github.com/Nxt-Stark/Instagram-dp-downloader")
    button4 = InlineKeyboardButton("Owner", url="https://t.me/NxtStark")
    button5 = InlineKeyboardButton("Help", url="https://www.youtube.com/c/HTechMedia")

    keyboard = InlineKeyboardMarkup([[button1, button2], [button3, button4],[button5]])

    await message.reply_photo(
        photo="https://telegra.ph/file/85a40fa28ea0f0d4db1c6.jpg",
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME), 
        reply_markup=keyboard
        parse_mode=enums.ParseMode.HTML)
    raise StopPropagation

@Client.on_message(filters.command(["help"]))
def help_msg(client, message):
    button1 = InlineKeyboardButton("Devoloper", url="https://t.me/NxtStark")
    button2 = InlineKeyboardButton("Support", url="https://t.me/HTechMediaSupport")
    button3 = InlineKeyboardButton("Youtube", url="https://www.youtube.com/c/HTechMedia")
    keyboard = InlineKeyboardMarkup([[button1, button2], [button3]])
    await message.reply_video(
        video="https://example.com/video.mp4",
        caption=script.HELP_TXT,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML)

ADMIN_USER_ID = 1180676984

@Client.on_message(filters.command("settings") & filters.user(ADMIN_ID))
async def opensettings(client, cmd):
    user_id = cmd.from_user.id
    await cmd.reply_text(
        f"`Here You Can Set Your Settings:`\n\nSuccessfully set notifications to **{await db.get_notif(user_id)}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"NOTIFICATION {'🔔' if ((await db.get_notif(user_id)) is True) else '🔕'}",
                        callback_data="notifon",
                    )
                ],
                [InlineKeyboardButton("❎", callback_data="closeMeh")],
            ]
        ),
    )
    
@Client.on_message(filters.private & filters.command("broadcast") & filters.user(ADMIN_USER_ID))
async def broadcast_handler_open(client, message):
    if message.reply_to_message is None:
        await message.delete()
    else:
        await broadcast(message, db)

@Client.on_message(filters.private & filters.command("stats") & filters.user(ADMIN_USER_ID))
async def sts(client, message: Message):
    total_users = await db.total_users_count()
    total_notif_users = await db.total_notif_users_count()
    
    await message.reply_text(
        text=f"**Total Users in Database 📂:** `{total_users}`\n\n**Total Users with Notification Enabled 🔔 :** `{total_notif_users}`",
        parse_mode="Markdown",
        quote=True
    )

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



