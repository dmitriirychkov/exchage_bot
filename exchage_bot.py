from telebot import TeleBot, types #подключили библиотеку telebot
from pycoingecko import CoinGeckoAPI #Подключили библиотеку coingecko
api = CoinGeckoAPI()
token = ' #Указать свой токен ' #токе
bot = TeleBot(token, parse_mode='html') #Содание бота
base_currency = '' #Создание переменной для фиата
coin_name = ''
price = ''
#обработка старта
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    bot.send_message(
        chat_id=message.chat.id, # id чата, в который необходимо направить сообщение
        text='Привет! Я умею выводить актуальный курс криптовалют\nВыбери нужную фиатную валюту:', # текст сообщения
        reply_markup=card_type_keybaord,
    )

#Обьект клавиатуры
card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_type_keybaord.row(
    types.KeyboardButton(text='usd'),
    types.KeyboardButton(text='rub'),
)
#Обработка сообщения
@bot.message_handler()
def message_handler(message: types.Message):
    global base_currency
    if (message.text == 'usd') or (message.text == 'rub'):
        base_currency = message.text #Задание значения для фиата
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Вы выбрали {message.text}  :)',
        )
        card_type_keybaord = types.ReplyKeyboardMarkup(resize_keyboard =True)
        card_type_keybaord.row(
            types.KeyboardButton(text='BTC'),
            types.KeyboardButton(text='ETH'),
        )       
        # второй ряд кнопок
        card_type_keybaord.row(
            types.KeyboardButton(text='LTC'),
            types.KeyboardButton(text='USDT'),
        )
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=f'Выберите валюту',
            reply_markup=card_type_keybaord
        )   
        bot.register_next_step_handler(msg,test)
    else:
        bot.send_message(
                    chat_id=message.chat.id,
                    text='Не понимаю тебя :(',
                )

def test(message: types.Message):
    if base_currency == "usd":
        tx = '$'
    else:
        tx = '₽'
    if message.text == 'BTC':
        coin_name = 'bitcoin'
        price = api.get_price(ids=coin_name, vs_currencies=base_currency)
        price = price[coin_name][base_currency]
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=f'Курс валюты {coin_name}:\n<code>{price}{tx}</code>'
        )
        bot.register_next_step_handler(msg,test)
    elif message.text == 'ETH':
        coin_name = 'ethereum'
        price = api.get_price(ids=coin_name, vs_currencies=base_currency)
        price = price[coin_name][base_currency]
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=f'Курс валюты {coin_name}:\n<code>{price}{tx}</code>'
        )
        bot.register_next_step_handler(msg,test)
    elif message.text == 'LTC':
        coin_name = 'litecoin'
        price = api.get_price(ids=coin_name, vs_currencies=base_currency)
        price = price[coin_name][base_currency]
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=f'Курс валюты {coin_name}:\n<code>{price}{tx}</code>'
        )
        bot.register_next_step_handler(msg,test)
    elif message.text == 'USDT':
        coin_name = 'tether'
        price = api.get_price(ids=coin_name, vs_currencies=base_currency)
        price = price[coin_name][base_currency]
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=f'Курс валюты {coin_name}:\n<code>{price}{tx}</code>'
        )
        bot.register_next_step_handler(msg,test)
       # msg = '/start'
       # bot.register_next_step_handler(msg, message_handler)
    else:
                # если текст не совпал ни с одной из кнопок 
                # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Не понимаю тебя1 :({message.text}',
        )
        return
    # и выводим пользователю
    

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
