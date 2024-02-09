
#(1) to work, install pytelegrambotapi: pip3 install pytelegrambotapi
#(2) install requests: pip3 install requests

import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

#Доступные валюты:
keys = {
    'доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR',
    'фунт':'GBP',
    'юань': 'CNY',
}

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message: telebot.types.Message):
    instructions = f"Добро пожаловать, {message.from_user.first_name} 😊! Чтобы узнать курс валют, отправьте сообщение в формате:\n"
    instructions += "<имя валюты, цену которой хотите узнать> <имя валюты, в которой хотите узнать цену первой валюты> <количество первой валюты>\n\n"
    instructions += "Например:\n"
    instructions += "доллар рубль 100\n\n"
    instructions += "На данный момент, к сожалению, работает только конвертация долларов в другие валюты 😔 \n\n"
    instructions += "Чтобы получить список доступных валют, введите /values."
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def send_values(message):
    # Отправляем информацию о доступных валютах
    # values = "Доступные валюты:"
    # for key in keys.keys():
    #       values = '\n'.join((values, key, ))

    values = "Доступные валюты:\n"
    for key in keys.keys():
        values += key + '\n'
    bot.send_message(message.chat.id, values)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        parts = message.text.split()
        base_currency, quote_currency, amount = parts[0].lower(), parts[1].lower(), float(parts[2])

        if base_currency not in keys:
            bot.send_message(message.chat.id, f"🤔 Валюта {base_currency} введена неверно или не поддерживается. Попробуйте ввести снова 😇!")
            return
        elif quote_currency not in keys:
            bot.send_message(message.chat.id,
                             f"🤔 Валюта {quote_currency} введена неверно или не поддерживается. Попробуйте ввести снова 😇!")
            return
        elif base_currency == quote_currency:
            bot.send_message(message.chat.id,
                             "🤔 Пожалуйста, убедитесь, что вы не ввели одну и ту же валюту в оба поля. Попробуйте снова 😇!")
            return

        converted_amount = CurrencyConverter.get_price(keys[base_currency], keys[quote_currency], amount)
        response_text = "По курсу на данный момент:\n"
        response_text += f"{amount} {keys[base_currency]} = {converted_amount} {keys[quote_currency]}"
        bot.send_message(message.chat.id, response_text)

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "🤔Неправильный формат сообщения. Пожалуйста, используйте формат: <валюта1> <валюта2> <сумма>")

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()
