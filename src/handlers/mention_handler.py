# handlers/mention_handler.py
import os
from telegram import Update, Poll
from telegram.ext import CallbackContext

from handlers.delete_handlers import delete_user_message, delete_message

DELETE_DELAY = int(os.getenv("DELETE_DELAY", 600)) 

def mention_handler(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.username  # Получаем имя пользователя бота
    text = update.message.text.lower()  # Приводим текст сообщения к нижнему регистру

    # Проверяем, упоминается ли бот
    if bot_username.lower() in text:
        # Создаем опрос
        question = "Перекур? \n‼️ Курение вредит вашему здоровью ‼️"
        options = ["🚬", "🚭"]

        # Отправляем опрос
        message = update.message.reply_poll(
            question=question, options=options, is_anonymous=False
        )

        # Планируем удаление сообщения пользователя
        context.job_queue.run_once(delete_user_message, DELETE_DELAY, context=update.message)

        # Планируем удаление опроса через заданное время
        context.job_queue.run_once(delete_message, DELETE_DELAY, context=message)
