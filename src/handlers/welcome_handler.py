# handlers/welcome_handler.py
from telegram import Update
from telegram.ext import CallbackContext

def welcome_handler(update: Update, context: CallbackContext) -> None:
    # Проверяем, добавлен ли бот в новый чат
    if (
        update.message.chat.type in ["group", "supergroup"]
        and update.message.new_chat_members
    ):
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                # Приветственное сообщение
                context.bot.send_message(
                    chat_id=update.message.chat.id,
                    text="Привет! Для того, чтобы позвать коллег на перекур, вызови меня!",
                )
