# handlers/delete_handlers.py
from telegram.ext import CallbackContext

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
