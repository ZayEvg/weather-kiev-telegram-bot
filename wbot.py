import telebot
import requests
from bs4 import BeautifulSoup
import re


def get_page(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    r = requests.get(url, headers=headers)
    with open('page.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
    return text


def parse_page(filename, url, day):
    get_page(url)
    result = []
    text = read_file(filename)

    soup = BeautifulSoup(text, features="html.parser")

    date = ''
    min_temp = ''
    max_temp = ''
    all_dates = soup.find_all('div', {'class': 'tab-content'})
    for item in all_dates:
        if item.find('div', {'class': 'date xs'}):
            which_day = re.findall('\w+', item.find('div', {'class': 'date xs'}).text)
            if which_day[0] == day:
                date_day = re.findall('\w{2}\,\s\d+\s\w{2,5}', item.find('div', {'class': 'date'}).text)
                date = '(' + which_day[0] + ') ' + date_day[0]
                temps = item.find_all('span', {'class': 'unit unit_temperature_c'})
                if len(temps) == 1:
                    min_temp = re.findall('[+-−]?\d+', str(temps))[0]
                    max_temp = re.findall('[+-−]?\d+', str(temps))[0]
                elif len(temps) == 2:
                    min_temp = re.findall('[+-−]?\d+', str(temps[0]))[0]
                    max_temp = re.findall('[+-−]?\d+', str(temps[1]))[0]
    result.append(date)
    result.append(min_temp)
    result.append(max_temp)
    return result


token = ''
bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Погода сегодня', 'Погода завтра')
remove = telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот для просмотра погоды в Киеве. Давай начнём!', reply_markup=keyboard)


@bot.message_handler(commands=['bye'])
def stop_message(message):
    bot.send_message(message.chat.id, "До скорых встреч!", reply_markup=remove)


@bot.message_handler(content_types=['text'])
def reply_text_message(message):
    if message.text.lower() == "погода сегодня":
        answer = parse_page('page.html', 'https://www.gismeteo.ua/weather-kyiv-4944/', 'Сегодня')
        msg_txt = '%s\nТемпература от %s до %s' % (answer[0], answer[1], answer[2])
        bot.send_message(message.chat.id, msg_txt)
    elif message.text.lower() == "погода завтра":
        answer = parse_page('page.html', 'https://www.gismeteo.ua/weather-kyiv-4944/', 'Завтра')
        msg_txt = '%s\nТемпература от %s до %s' % (answer[0], answer[1], answer[2])
        bot.send_message(message.chat.id, msg_txt)


bot.polling()
