import logging

from telegram.ext.filters import BaseFilter
from contextlib import closing
from db import get_connection

logger = logging.getLogger(__name__)


class FilterNewChatMembers(BaseFilter):
    """ Filtering entering messages  """

    def __init__(self):
        logger.info("Get user statuses for the captcha")
        self.status_members = ["member", "restricted", "left", "kicked"]

    def __call__(self, update):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        message = update.effective_message
        logger.info("Get data base connection")
        db_connection = get_connection()

        if message.new_chat_members:
            logger.info("Checking if user has already received captcha")
            with closing(db_connection.cursor()) as cur:
                cur.execute("SELECT id FROM banlist WHERE chat_id=%s AND user_id=%s" % (chat_id, user_id))
                if cur.fetchone():
                    return False

            member_status = message.bot.getChatMember(chat_id, user_id)["status"]
            if member_status in self.status_members:
                return True
        return False
