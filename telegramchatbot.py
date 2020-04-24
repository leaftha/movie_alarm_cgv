import requests
import telepot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = '1018659286:AAFcAg5VqnM_miAWgijd0v3Iybu7cBmb9Vo'


def check_id(bot, update):
    try:
        id = update.message.chat.id
        print('Chat ID', id)
        return id
    except:
        id = update.channel_post.chat.id
        return id

def check_nickname(bot, update):
    try:
        nickname = update.message.from_user.first_name
        print('Chat NickName', nickname)
        return nickname
    except:
        nickname = update.channel_post.from_user.first_name
        return nickname

def start_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    bot.send_message(chat_id=id, text="안녕하세요 " + nickname +"! 실험용 챗봇OO입니다!\n\n")

def movie_command(bot, update):
    id = check_id(bot, update)
    toyear = str(datetime.today().year)
    tomonth = str(datetime.today().month)
    today = str(datetime.today().day)
    time = str(toyear + tomonth + today)
    url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=P013&date=' + time + '&screencodes=&screenratingcode=09&regioncode=103'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    title_list = soup.select('div.col-times')
    for i in title_list:
        title = i.select_one('div.info-movie> a > strong').text.strip()
        title_time = i.select_one(' div.info-timetable > ul > li > a > em').text.strip()
        bot.sendMessage(chat_id=id, text=title + "의 상영시간\n" + title_time)

    bot.sendMessage(chat_id=id, text="이상이 " + time + "의 영화 시간표입니다")

def help_command(bot, update):
    id = check_id(bot,update)
    bot.sendMessage(chat_id=id ,text="지금까지의 명려어 \n /start \n /movie \n /input \n /list \n 가 구현되었습니다.")


def input_command(bot, update):
    id = check_id(bot,update)
    global msg
    msg = update.message.text.split()
    del msg[0]
    # return msg

def list_command(bot, update):
    id = check_id(bot, update)
    for i in msg:
        bot.sendMessage(chat_id=id, text=i)

def check_command(bot, update):
    id = check_id(bot, update)

    for i in range(len(msg)):
        global count
        count = i + 1
        a = str(count)
        message = '제' + a + '번 할일 입니다.'
        task_buttons = [[InlineKeyboardButton(msg[i], callback_data=count)]]
        reply_markup = InlineKeyboardMarkup(task_buttons)
        bot.send_message(
            chat_id=id
            , text= message
            , reply_markup=reply_markup
        )


def buttoncallback_cammand(bot, update):
    id = check_id(bot, update)
    query = update.callback_query
    data = query.data

    bot.send_chat_action(
        chat_id=id
        , action=ChatAction.TYPING
    )
    for i in range(1, count):
        if data == count:
            bot.sen_message(chat_id=update.callback_query.message.chat_id, text='번 일을 했습니다.', message_id=update.callback_query.message.message_id)

def test_command(bot, update):
    id = check_id(bot, update)
    bot.send_message(chat_id=id, text="작동1")

    testlist = ["운동", "과제", "공부"]
    for i in range(len(testlist)):
        a = str(i+1)
        message = '제' + a + '번 할일 입니다.'
        bot.send_message(chat_id=id, text="작동2")
        task_buttons = [[InlineKeyboardButton(testlist[i], callback_data=i + 1)]]
        reply_markup = InlineKeyboardMarkup(task_buttons)
        bot.send_message(chat_id=id, text="작동3")
        bot.send_message(
            chat_id=id
            , text=message
            , reply_markup=reply_markup
        )

def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    if callback_header != "" :
        text_header += ","

    for text in text_list :
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('movie', movie_command))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CommandHandler('input', input_command))
updater.dispatcher.add_handler(CommandHandler('list', list_command))
updater.dispatcher.add_handler(CommandHandler('check', check_command))
updater.dispatcher.add_handler(CallbackQueryHandler( buttoncallback_cammand ))
updater.dispatcher.add_handler(CommandHandler('test', test_command))



updater.start_polling(poll_interval=0.0,
                          timeout=10,
                          clean=False,
                          bootstrap_retries=0)
updater.idle()
