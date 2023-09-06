import logging
import os
import sqlite3

logger = logging.getLogger(__name__)
DB_FILE = os.environ.get("DB_FILE", './chatbot.db')
_db_connection = None


def create_db():
    logger.info("Creating a new data base")
    db_connection = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = db_connection.cursor()
    logger.info("Creating a table banlist in data base")
    cur.execute(
        """
        CREATE TABLE banlist
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INT NOT NULL,
        time timestamp NOT NULL,
        chat_id BIGINT NOT NULL,
        captcha_message_id INT NOT NULL,
        answer INT NOT NULL);
    """

    )
    db_connection.commit()
    logger.info("Closing connection")
    db_connection.close()


def get_connection():
    global _db_connection
    if not _db_connection:
        if not os.path.isfile(DB_FILE):
            create_db()
        logger.info("Creating a new db connection")
        _db_connection = sqlite3.connect(DB_FILE, check_same_thread=False)
    return _db_connection

