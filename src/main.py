# main.py
import os
from dotenv import load_dotenv
load_dotenv()
from telegram.ext import Updater, MessageHandler, Filters

from handlers.mention_handler import mention_handler
from handlers.welcome_handler import welcome_handler

API_TOKEN = os.getenv("TOKEN")


def main() -> None:
    updater = Updater(API_TOKEN)

    # Обработка упоминания бота
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, mention_handler)
    )

    # Обработка добавления бота в чат
    updater.dispatcher.add_handler(
        MessageHandler(Filters.status_update.new_chat_members, welcome_handler)
    )

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
