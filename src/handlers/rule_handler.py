# handlers/rule_handler.py
from telegram import Update
from telegram.ext import CallbackContext

def rule_handler(update: Update, context: CallbackContext) -> None:
    # Отправляем правила работы бота
    rules_message = (
        "👋 Привет!\n"
        "Я SmokerBot.\n"
        "Вот как я работаю:\n"
        "1. Добавте меня в чат и упомяните, чтобы запустить опрос о перекуре.\n"
        "2. Я удалю сообщение и опрос через 10 минут.\n"
        "О проекте можно почитать здесь: https://github.com/madvln/telbot\n\n"
        "‼️ Курение вредит вашему здоровью ‼️\n\n"
    )
    update.message.reply_text(rules_message)