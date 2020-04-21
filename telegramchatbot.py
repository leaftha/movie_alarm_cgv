import requests
import telepot
from telegram.ext import Updater, CommandHandler
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

def movie_commad(bot, update):
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

def help_commad(bot, update):
    id = check_id(bot,update)
    bot.sendMessage(chat_id=id ,text="지금까지의 명려어 \n /start \n /movie \n /input \n /list \n 가 구현되었습니다.")


def input_commad(bot, update):
    id = check_id(bot,update)
    global msg
    msg = update.message.text.split()
    del msg[0]
    bot.sendMessage(chat_id=id ,text=msg)
    return msg

def list_commad(bot, update):
    id = check_id(bot, update)
    for i in msg:
        bot.sendMessage(chat_id=id, text=i)


updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('movie', movie_commad))
updater.dispatcher.add_handler(CommandHandler('help', help_commad))
updater.dispatcher.add_handler(CommandHandler('input', input_commad))
updater.dispatcher.add_handler(CommandHandler('list', list_commad))

updater.start_polling(poll_interval=0.0,
                          timeout=10,
                          clean=False,
                          bootstrap_retries=0)
updater.idle()
