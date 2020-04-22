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

def cmd_task_buttons(bot, update):
    id = check_id(bot, update)
    bot.send_message(chat_id=id, text="작동2")
    for i in range(len(msg)):
        task_buttons = [[InlineKeyboardButton(msg[i], callback_data=i + 1)]]
        reply_markup = InlineKeyboardMarkup(task_buttons)
        bot.send_message(
            chat_id=id
            , text= i+1
            , reply_markup=reply_markup
        )


# def cb_button(bot, update):
#     query = update.callback_query
#     data = query.data
#
#     bot.send_chat_action(
#         chat_id=update.effective_user.id
#         , action=ChatAction.TYPING
#     )
#
#     if data == '3':
#         bot.edit_message_text(
#             text='작업이 취소되었습니다.'
#             , chat_id=query.message.chat_id
#             , message_id=query.message.message_id
#         )
#     else:
#         bot.edit_message_text(
#             text='[{}] 작업이 진행중입니다.'.format(data)
#             , chat_id=query.message.chat_id
#             , message_id=query.message.message_id
#         )
#
#         if data == '1':
#             crawl_navernews()
#         elif data == '2':
#             crawl_zigbang()
#
#         context.bot.send_message(
#             chat_id=update.effective_chat.id
#             , text='[{}] 작업을 완료하였습니다.'.format(data)
#         )

def test_command(bot, update):
    id = check_id(bot, update)
    bot.send_message(chat_id=id, text="작동2")

    testlist = ["운동", "과제", "공부"]
    for i in range(len(testlist)):
        task_buttons = [[InlineKeyboardButton(testlist[i], callback_data=i + 1)]]
        reply_markup = InlineKeyboardMarkup(task_buttons)
        bot.sendMessage(
            chat_id=id
            , text= i+1
            , reply_markup=reply_markup
        )

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('movie', movie_command))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CommandHandler('input', input_command))
updater.dispatcher.add_handler(CommandHandler('list', list_command))
updater.dispatcher.add_handler(CommandHandler('button', cmd_task_buttons))
updater.dispatcher.add_handler(CommandHandler('test', test_command))


updater.start_polling(poll_interval=0.0,
                          timeout=10,
                          clean=False,
                          bootstrap_retries=0)
updater.idle()
