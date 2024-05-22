import telebot

import extensions
import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handler_start_help(message: telebot.types.Message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
        bot.send_message(message.chat.id, f'Вот доступные команды:\n{config.commands_text}')
    elif message.text == '/help':
        bot.send_message(message.chat.id, f'Список команд:\n{config.commands_text}')


@bot.message_handler(commands=['values'])
def handler_command(message: telebot.types.Message):
    if message.text == '/values':
        c = '\n'.join(config.currency.keys())
        bot.reply_to(message, f'Cписок валют:\n{c}')


@bot.message_handler(content_types=['text'])
def handler_message(message: telebot.types.Message):
    if message.text:
        try:
            extensions.Converter.is_currency(message)
            text = message.text.split()
            text = config.currency[text[0].title()], config.currency[text[1].title()], float(text[2])
            bot.send_message(message.chat.id, extensions.Converter.get_price(text[0], text[1], text[2]))
        except extensions.APIException as e:
            bot.send_message(message.chat.id, e)
        except Exception as e:
            bot.send_message(message.chat.id, e)


bot.polling(none_stop=True)
