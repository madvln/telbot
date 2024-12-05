from telegram import Update, ChatMember, Poll, ParseMode
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
print(API_TOKEN)


# Функция для проведения опроса
def create_poll(
    update: Update,
    context: CallbackContext,
    question: str,
    options: list,
    individual_user_id=None,
) -> None:
    if individual_user_id:
        # Отправляем опрос конкретному пользователю
        context.bot.send_poll(
            chat_id=individual_user_id,
            question=question,
            options=options,
            is_anonymous=False,
        )
    else:
        # Отправляем опрос в общий чат
        message = update.message.reply_poll(
            question=question, options=options, is_anonymous=False
        )

        # Планируем удаление сообщения пользователя и опроса через 10 секунд
        context.job_queue.run_once(delete_user_message, 10, context=update.message)
        context.job_queue.run_once(delete_message, 10, context=message)


# Функция для обработки сообщений и проверки упоминания бота
def mention_handler(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.username  # Получаем имя пользователя бота
    text = update.message.text.lower()  # Приводим текст сообщения к нижнему регистру

    # Проверяем, упоминается ли бот
    if bot_username.lower() in text:
        # Извлекаем команду из текста
        if "всем" in text:
            question = "Вы упомянули меня! Хотите продолжить?"
            options = ["Да", "Нет"]
            create_poll(update, context, question, options)  # Опрос для всех участников
        elif "@" in text:
            # Извлекаем ID пользователя из упоминания
            user_mention = text.split("@")[-1].strip()
            print(user_mention, "!!!!!!!!!!!")
            print(update.message.chat)
            print(update.message.chat.get_member(user_id=1))
            # Поиск пользователя в чате
            for member in update.message.chat.members:
                if member.user.username == user_mention:
                    question = "Вы упомянули меня! Хотите продолжить?"
                    options = ["Да", "Нет"]
                    create_poll(
                        update,
                        context,
                        question,
                        options,
                        individual_user_id=member.user.id,
                    )  # Опрос для конкретного пользователя
                    return


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
                    text="Привет! Я ваш новый бот. Как я могу вам помочь? 🤖✨",
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
