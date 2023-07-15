import logging
from pyrogram.raw.all import layer
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
from pyrogram import Client, __version__, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.broadcast import broadcast
from handlers.check_user import handle_user_status
from handlers.database import Database
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, APP_NAME, TELEGRAM_USERNAME, DB_URL, DB_NAME, LOG_CHANNEL, BROADCAST_AS_COPY

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = "@" + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

app = Bot()
app.run()
