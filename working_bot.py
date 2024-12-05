from telegram import Update, ChatMember
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
    ChatMemberHandler,
)
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("TOKEN")


# Функция для обработки сообщений и проверки упоминания бота
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
        context.job_queue.run_once(delete_user_message, 60 * 10, context=update.message)

        # Планируем удаление опроса через 60*10 секунд
        context.job_queue.run_once(delete_message, 60 * 10, context=message)


# Функция для обработки добавления бота в чат
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


def delete_user_message(context: CallbackContext) -> None:
    # Удаляем сообщение с упоминанием бота
    context.bot.delete_message(
        chat_id=context.job.context.chat.id, message_id=context.job.context.message_id
    )


def delete_message(context: CallbackContext) -> None:
    # Удаляем сообщение с опросом
    context.bot.delete_message(
        chat_id=context.job.context.chat.id, message_id=context.job.context.message_id
    )


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
