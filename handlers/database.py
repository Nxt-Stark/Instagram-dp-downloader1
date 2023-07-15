import datetime
from pyrogram import Client
from pyrogram.types import ChatPermissions


class Database:
    def __init__(self, url, name):
        self.url = url
        self.name = name

    async def new_user(self, chat_id):
        return {
            "chat_id": chat_id,
            "join_date": datetime.date.today().isoformat(),
            "notif": True,
            "ban_status": {
                "is_banned": False,
                "ban_duration": 0,
                "banned_on": datetime.date.max.isoformat(),
                "ban_reason": "",
            },
        }

    async def add_user(self, chat_id):
        user = await self.new_user(chat_id)
        await self.client.add_chat(chat_id, user)

    async def is_user_exist(self, chat_id):
        return await self.client.chat_exists(chat_id)

    async def total_users_count(self):
        return len(await self.client.get_all_chats())

    async def get_all_users(self):
        return await self.client.get_all_chats()

    async def delete_user(self, chat_id):
        await self.client.delete_chat(chat_id)

    async def remove_ban(self, chat_id):
        ban_status = {
            "is_banned": False,
            "ban_duration": 0,
            "banned_on": datetime.date.max.isoformat(),
            "ban_reason": "",
        }
        await self.client.update_chat(chat_id, {"ban_status": ban_status})

    async def ban_user(self, chat_id, ban_duration, ban_reason):
        ban_status = {
            "is_banned": True,
            "ban_duration": ban_duration,
            "banned_on": datetime.date.today().isoformat(),
            "ban_reason": ban_reason,
        }
        await self.client.update_chat(chat_id, {"ban_status": ban_status})
        # Apply chat permissions for banned users (optional)
        await self.client.restrict_chat_member(
            chat_id=chat_id,
            user_id=chat_id,
            permissions=ChatPermissions(),
            until_date=datetime.datetime.now() + datetime.timedelta(seconds=ban_duration),
        )

    async def get_ban_status(self, chat_id):
        default = {
            "is_banned": False,
            "ban_duration": 0,
            "banned_on": datetime.date.max.isoformat(),
            "ban_reason": "",
        }
        chat = await self.client.get_chat(chat_id)
        return chat.get("ban_status", default)

    async def get_all_banned_users(self):
        return await self.client.get_all_chats({"ban_status.is_banned": True})

    async def set_notif(self, chat_id, notif):
        await self.client.update_chat(chat_id, {"notif": notif})

    async def get_notif(self, chat_id):
        chat = await self.client.get_chat(chat_id)
        return chat.get("notif", False)

    async def get_all_notif_user(self):
        return await self.client.get_all_chats({"notif": True})

    async def total_notif_users_count(self):
        return len(await self.client.get_all_chats({"notif": True}))


# Usage example:
async def main():
    client = Client("my_bot")
    await client.start()

    database = Database(client)

    # Accessing methods
    await database.add_user(123456789)  # Add a new user
    exist = await database.is_user_exist(123456789)  # Check if user exists
    count = await database.total_users_count()  # Get total users count

    await client.stop()


if __name__ == '__main__':
    asyncio.run(main())
