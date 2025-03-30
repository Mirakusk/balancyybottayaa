from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Токен твоего бота
TOKEN = "7976551003:AAGeq6RoOsg_BbV1ZVaLMWTeCgLsFngvRWs"

# Словарь для хранения валютных счетов пользователей (по username)
user_balances = {}

# ID авторизованных пользователей (можно добавить несколько ID)
AUTHORIZED_USERS = [2145894494, 6528463797]  # Замените на реальные ID пользователей

# Функция для проверки авторизованного пользователя
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для управления валютой. Используй /balance, /add, /remove и /setbalance.")

# Команда /balance - проверка баланса пользователя
def balance(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    if username in user_balances:
        update.message.reply_text(f"Твой текущий баланс: {user_balances[username]} валюты.")
    else:
        update.message.reply_text("У тебя еще нет валюты. Используй команду /add для добавления.")

# Команда /add - добавление валюты
def add(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    try:
        # Если указан username другого пользователя
        if len(context.args) == 2:
            target_username = context.args[0]  # username пользователя
            amount = int(context.args[1])  # количество валюты

            if target_username in user_balances:
                user_balances[target_username] += amount
            else:
                user_balances[target_username] = amount
            update.message.reply_text(f"Ты добавил {amount} валюты пользователю @{target_username}.")
        
        # Если не указан username, добавляем валюту себе
        elif len(context.args) == 1:
            amount = int(context.args[0])  # количество валюты
            if username in user_balances:
                user_balances[username] += amount
            else:
                user_balances[username] = amount
            update.message.reply_text(f"Ты добавил {amount} валюты. Твой новый баланс: {user_balances[username]}")
        
        else:
            update.message.reply_text("Пожалуйста, укажи количество валюты.")
    
    except (IndexError, ValueError):
        update.message.reply_text("Пожалуйста, укажи корректное количество валюты.")

# Команда /remove - удаление валюты
def remove(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    try:
        # Если указан username другого пользователя
        if len(context.args) == 2:
            target_username = context.args[0]  # username пользователя
            amount = int(context.args[1])  # количество валюты

            if target_username in user_balances and user_balances[target_username] >= amount:
                user_balances[target_username] -= amount
                update.message.reply_text(f"Ты удалил {amount} валюты у пользователя @{target_username}.")
            else:
                update.message.reply_text(f"Недостаточно средств для пользователя @{target_username}.")
        
        # Если не указан username, удаляем валюту себе
        elif len(context.args) == 1:
            amount = int(context.args[0])  # количество валюты
            if username in user_balances and user_balances[username] >= amount:
                user_balances[username] -= amount
                update.message.reply_text(f"Ты удалил {amount} валюты. Твой новый баланс: {user_balances[username]}")
            else:
                update.message.reply_text("Недостаточно средств.")
        
        else:
            update.message.reply_text("Пожалуйста, укажи количество валюты.")
    
    except (IndexError, ValueError):
        update.message.reply_text("Пожалуйста, укажи корректное количество валюты.")

# Команда /setbalance - изменение баланса другого пользователя по username
def setbalance(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    if not is_authorized(update.message.from_user.id):
        update.message.reply_text("У тебя нет доступа к этой команде.")
        return
    try:
        target_username = context.args[0]  # username пользователя
        new_balance = int(context.args[1])  # новый баланс
        if target_username in user_balances:
            user_balances[target_username] = new_balance
        else:
            user_balances[target_username] = new_balance
        update.message.reply_text(f"Баланс пользователя @{target_username} был изменен на {new_balance}.")
    except (IndexError, ValueError):
        update.message.reply_text("Пожалуйста, укажи username пользователя и новый баланс.")

# Обработчик команды /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Команды:\n"
        "/start - Приветствие\n"
        "/balance - Проверить баланс\n"
        "/add <username> <amount> - Добавить валюту другому пользователю\n"
        "/remove <username> <amount> - Удалить валюту у другого пользователя\n"
        "/setbalance <username> <new_balance> - Установить новый баланс для другого пользователя"
    )

def main():
    # Создаем и настраиваем бота
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("setbalance", setbalance))
    dispatcher.add_handler(CommandHandler("help", help))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
