# For @UniBorg
# (c) Shrimadhav U K

from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights


CHATS_TO_MONITOR_FOR_ADDED_BOTS = [
    # add the ID of the groups (Use .get_id command)
    # seperated by commas
    # usernames also work, but it is pointless,
    # since non admin users cannot add bots to
    # public groups (Telegram Limitation)
]


@borg.on(events.ChatAction(chats=CHATS_TO_MONITOR_FOR_ADDED_BOTS))
async def kick_if_bots(event):
    if event.user_added:
        users_added_by = event.action_message.from_id
        if users_added_by == borg.uid:
            logger.info("Don't BAN yourself")
            return False
        is_ban_able = False
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True
        )
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await borg.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                try:
                    # kick the bot
                    await borg(EditBannedRequest(event.chat_id, user_obj, rights))
                except Exception as e:
                    logger.warn(str(e))
                    # maybe you don't have admin priveleges here :\
                    pass
        if is_ban_able:
            # this is required if the group has a group administration bot
            ban_reason_msg = await event.reply("!warn [user](tg://user?id={}) Please Do Not Add BOTs to this chat.".format(users_added_by))
