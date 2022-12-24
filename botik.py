import telebot  # pip install pyTelegramBotAPI
import requests
import random
from bs4 import BeautifulSoup
from telebot import types

# НЕ ЗАБУДЬТЕ ВСТАВИТЬ СВОЙ ТОКЕН!!!!
token = '5821269212:AAHgGkwH7AE0t8V_ktqqREBSBx5jMDmvTQQ'
bot = telebot.TeleBot(token)


# /start  /help
@bot.message_handler(commands=['start', 'help'])
def sennd_welcome(message):
    # Создаём клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    # Создаём кнопки
    button_poem = types.KeyboardButton('Стихотворение')
    button_fact = types.KeyboardButton('Факт')
    button_cat = types.KeyboardButton('Кот')
    button_music = types.KeyboardButton('Песня')
    button_game = types.KeyboardButton('Игра')
    button_bestgame = types.KeyboardButton('Рекомендация игры по жанру')
    # Добавляем кнопки
    keyboard.add(button_poem, button_fact, button_cat, button_music, button_game)
    keyboard.add(button_bestgame)

    welcome_text = 'Привет! Я умею рассказывать стихи, знаю много интересных фактов и могу показать милых котиков!'
    # Отправляем клавиатуру
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


# /poem
@bot.message_handler(commands=['poem'])
def send_poem(message):
    poem_text = "Муха села на варенье, вот и все стихотворенье..."
    bot.send_message(message.chat.id, poem_text)
    keybord = types.InlineKeyboardMarkup(row_width=1)
    button_url = types.InlineKeyboardButton('Перейти', url='https://stihi.ru/')
    keybord.add(button_url)
    bot.send_message(message.chat.id, 'Больше стихов по ссылке ниже', reply_markup=keybord)


# /fact
@bot.message_handler(commands=['fact'])
def send_fact(message):
    content = requests.get('https://i-fakt.ru/').content
    html = BeautifulSoup(content, 'html.parser')
    fact = random.choice(html.find_all(class_='p-2 clearfix'))
    bot.send_message(message.chat.id, fact.text)
    fact_link = fact.a.attrs['href']
    bot.send_message(message.chat.id, fact_link)


# /cat
@bot.message_handler(commands=['cat'])
def send_cat(message):
    cat_number = str(random.randint(1, 10))
    cat_img = open('img/' + cat_number + '.jpg', 'rb')
    bot.send_photo(message.chat.id, cat_img)


# /music
@bot.message_handler(commands=['music'])
def send_music(message):
    song = open('happy.mp3', 'rb')
    bot.send_audio(message.chat.id, song)


# /sticker
@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGyAFjlcn6NwXCN0gfFcJfQ-iv-usiUAAC1CIAAvhtsEgTy0IAAWSuHYgrBA')


@bot.message_handler(commands=['game'])
def game(message):
    games = ['The Witcher 3: Wild Hunt', 'Grand Theft Auto V', 'Red Dead Redemption 2', 'Resident Evil 2: Remake',
             'Half-Life: Alyx', 'Mass Effect 2', 'Horizon Zero Dawn', 'Battlefield 3', 'The Elder Scrolls 5: Skyrim',
             "Assassin's Creed 2"]
    game = random.choice(games)
    bot.send_message(message.chat.id, f'Рекомендую игру: {game}')


@bot.message_handler(commands=['bestgame'])
def bestgame(message):
    global genrename,genrelist

    genrelist = []

    response = requests.get('https://www.igromania.ru/games/')
    response = response.content
    html = BeautifulSoup(response, 'lxml')
    genres = html.find(class_='title', string='Жанры').find_all_next(class_='element')
    k = 0
    for genrehtml in genres:
        k += 1
        genretext = genrehtml.text.strip()
        genrename = genretext.partition('			')[0]
        genreeng = genrehtml['href'].split('/')[3]
        genrehref = f"https://www.igromania.ru/games/games/{genreeng}"
        genref = {'num': k, 'name': genrename, 'href': genrehref}
        genrelist.append(genref)
        gamemess = f'{k}: {genrename}'
        if k == 23:
            break
        mess = f'{k}: {genrename}'
        bot.send_message(message.chat.id, mess)

    choose = bot.reply_to(message, 'Выбери номер жанра')
    bot.register_next_step_handler(choose, ugame)


def ugame(message):
    choose = message.text
    inputgenre = genrelist[int(choose) - 1]
    inputgenrehref = inputgenre.get('href')
    response = requests.get(inputgenrehref)
    response = response.content
    html = BeautifulSoup(response, 'lxml')
    bestgame = html.find(class_="name")
    mess = bestgame.text.strip()
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.strip() == 'Стихотворение':
        send_poem(message)
    elif message.text.strip() == 'Факт':
        send_fact(message)
    elif message.text.strip() == 'Кот':
        send_cat(message)
    elif message.text.strip() == 'Песня':
        send_music(message)
    elif message.text.strip() == 'Игра':
        game(message)
    elif message.text.strip() == 'Рекомендация игры по жанру':
        bestgame(message)
    else:
        bot.send_message(message.chat.id, 'Пока')


bot.polling(none_stop=True)
