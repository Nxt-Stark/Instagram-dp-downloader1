import datetime
import logging
from info import DB_URL, DB_NAME, LOG_CHANNEL
from pyrogram import Client
from handlers.database import Database

DB_URL = DB_URL
DB_NAME = DB_NAME
LOG_CHANNEL = LOG_CHANNEL

db = Database(DB_URL, DB_NAME)

async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await bot.send_message(
                LOG_CHANNEL,
                f"#NEWUSER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{BOT_USERNAME} !!",
            )
        else:
            logging.info(f"#NewUser :- Name : {cmd.from_user.first_name} ID : {cmd.from_user.id}")

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
            datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned to Use This Bot ", quote=True)
            return
    await cmd.continue_propagation()


# Usage example:
async def main():
    bot = Client("my_bot", bot_token=config.BOT_TOKEN)
    bot.add_handler(handle_user_status)

    await bot.start()

    # Run your other bot functionality here

    await bot.idle()
    await bot.stop()


if __name__ == '__main__':
    asyncio.run(main())
