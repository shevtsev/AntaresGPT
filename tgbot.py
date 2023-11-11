import openai as ai
import telebot
import threading
from gigachat import GigaChat
import urllib.request as ur

#TOKENS
ai.api_key ="sk-bxtDOY1i9Ndeav5mbP9fDh7d7Ccp4G2l"
gigatoken = "Mzg5Yjc1NjEtNDUwMi00NGNmLTgzNTMtYzE4OTA4N2JkYTNlOmM3NzI1MDYwLWM3M2ItNGUwYS04NjBjLTVhNDdlZTVkMzczMA=="
ai.api_base = "https://api.proxyapi.ru/openai/v1"

#tg bot
token = '6562461229:AAEwTPvnp8AZfKtTG8Vvy5jwIfdC_zUg50Y'
bot=telebot.TeleBot(token)

#start
@bot.message_handler(commands=['start'])
def GPT_function(message):    
    threading.Thread(target=process_request,
                     args=(bot, message)).start()
def process_request(bot, message):
    bot.send_message(message.chat.id,
                     "Привет, я AntaresGPT бот, здесь есть Chat GPT, Giga Chat и DALLE 2! Пользуйся",
                     parse_mode='html')

#GPT 3.5
@bot.message_handler(commands=['t'])
def GPT3_function(message):    
    threading.Thread(target=gpt3_request,
                     args=(bot, message)).start()
def gpt3_request(bot, message):
    if message.text[2:]!='':
        msg = bot.send_message(message.chat.id,
                               "Подождите, это должно занять несколько секунд",
                               parse_mode='html')
        try:
            chat_completion = ai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                       messages=[{"role": "user", "content": message.text[2:]}])
        except ai.api_errors.PaymentRequiredError:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=msg.message_id,
                                  text="Недостаточно средств на балансе аккаунта OpenAI",
                                  parse_mode='html')
        else:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=msg.message_id,
                                  text=chat_completion.choices[0]['message']['content'],
                                  parse_mode='html')
    else:
        bot.send_message(message.chat.id,
                         "Введите ваш запрос",
                         parse_mode='html')

#GPT 4
@bot.message_handler(commands=['t4'])
def GPT4_function(message):    
    threading.Thread(target=gpt4_request,
                     args=(bot, message)).start()
def gpt4_request(bot, message):
    if message.text[3:]!='':
        msg = bot.send_message(message.chat.id,
                               "Подождите, это должно занять несколько секунд",
                               parse_mode='html')
        try:
            chat_completion = ai.ChatCompletion.create(model="gpt-4",
                                                       messages=[{"role": "user", "content": message.text[3:]}])
        except ai.api_errors.PaymentRequiredError:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=msg.message_id,
                                  text="Недостаточно средств на балансе аккаунта OpenAI",
                                  parse_mode='html')
        else:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=msg.message_id,
                                  text=chat_completion.choices[0]['message']['content'],
                                  parse_mode='html')
    else:
        bot.send_message(message.chat.id,
                         "Введите ваш запрос",
                         parse_mode='html')

#Sber Giga Chat
@bot.message_handler(commands=['giga'])
def giga_function(message):    
    threading.Thread(target=giga_request,
                     args=(bot, message)).start()
def giga_request(bot, message):
    if message.text[5:]!='':
        msg = bot.send_message(message.chat.id,
                               "Подождите, это должно занять несколько секунд",
                               parse_mode='html')
        with GigaChat(credentials=gigatoken,
                        verify_ssl_certs=False) as giga:
            response = giga.chat(message.text[5:])
        bot.edit_message_text(chat_id=message.chat.id,
                                message_id=msg.message_id,
                                text=response.choices[0].message.content,
                                parse_mode='html')
    else:
        bot.send_message(message.chat.id,
                         "Введите ваш запрос",
                         parse_mode='html')

#DALLE-2
@bot.message_handler(commands=['dalle'])
def handle_imagine(message):
    threading.Thread(target=dalle_request,
                     args=(bot, message)).start()
def dalle_request(bot, message):
    if message.text[6:]!='':
        msg = bot.send_message(message.chat.id,
                               "Подождите, это должно занять несколько секунд",
                               parse_mode='html')
        try:
            response = ai.Image.create(
                prompt=message.text[6:],
                n=1,
                size="256x256"
            )
        except ai.error.APIError:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=msg.message_id,
                                  text="Некоректный запрос. Введите ваш запрос",
                                  parse_mode='html')
        except ai.api_errors.PaymentRequiredError:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=msg.message_id,
                                  text="Недостаточно средств на балансе аккаунта OpenAI",
                                  parse_mode='html')
        else:
            r = ur.urlopen(response['data'][0]['url'])
            with open("images/img1.png", "wb") as photo:
                photo.write(r.read())
            with open("images/img1.png", "rb") as photo:
                bot.delete_message(message.chat.id,
                                   msg.message_id)
                bot.send_photo(message.chat.id,
                               photo)
    else:
        bot.send_message(message.chat.id,
                         "Введите ваш запрос",
                         parse_mode='html')

#run
bot.infinity_polling()