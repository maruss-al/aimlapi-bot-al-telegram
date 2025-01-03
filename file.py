from openai import OpenAI
import telebot
import time

# Токены и настройки
telegram_key = '8140711563:AAFiF9xP-LSNIIx545RwQ3fLa5vG2Un-NRY'
base_url = "https://api.aimlapi.com/v1"
api_key = "6ab20dd6bc7d4b599682f61e130a06af"
system_prompt = "Вы программист и знаете все и умеете писать сочинения и изложения и вы знаете себя полностью, но самое главное, вы программист высшего уровня"

# Инициализация API и бота
api = OpenAI(api_key=api_key, base_url=base_url)
bot = telebot.TeleBot(telegram_key)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет, я твой GPT BYS. Я готов тебе помочь!')

@bot.message_handler(content_types=['text'])
def main(message):
    # Отправляем сообщение "Думает..."
    thinking_message = bot.send_message(message.chat.id, 'Думает...')

    # Получаем ответ от API
    completion = api.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message.text},
        ],
        temperature=0.7,
        max_tokens=512,
        stop=None
    )

    reply = ''
    if completion and completion.choices:
        reply = completion.choices[0].message.content.strip()
    else:
        reply = 'Что-то пошло не так.'

    # Удаляем сообщение "Думает..."
    bot.delete_message(thinking_message.chat.id, thinking_message.message_id)

    # Отправляем ответ от GPT
    bot.send_message(message.chat.id, reply)

# Запуск бота
bot.polling(none_stop=True)
