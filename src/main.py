# main.py
import os
from dotenv import load_dotenv

# Загружаем .env, если он есть
load_dotenv()

# Получаем токен из переменной окружения
API_TOKEN = os.getenv("TOKEN")

# Проверяем, задан ли токен
if not API_TOKEN:
    # Если токен не найден, попробуем загрузить из Secrets GitHub
    API_TOKEN = os.environ.get("TOKEN")
    if not API_TOKEN:
        raise ValueError(
            "Telegram API token is not set. Please provide it via .env file or as an environment variable."
        )
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from handlers.mention_handler import mention_handler
from handlers.welcome_handler import welcome_handler
from handlers.rule_handler import rule_handler


def main() -> None:
    updater = Updater(API_TOKEN)

    # Обработка команды /start
    updater.dispatcher.add_handler(CommandHandler("start", rule_handler))

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
