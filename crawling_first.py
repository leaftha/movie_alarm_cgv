import requests
import telegram
from bs4 import BeautifulSoup
from datetime import datetime


toyear = str(datetime.today().year)
tomonth = str(datetime.today().month)
today = str(datetime.today().day)
time = str(toyear+tomonth+today)
bot = telegram.Bot(token = '1018659286:AAFcAg5VqnM_miAWgijd0v3Iybu7cBmb9Vo')
url ='http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=P013&date='+time+'&screencodes=&screenratingcode=09&regioncode=103'
html = requests.get(url)
soup = BeautifulSoup(html.text,'html.parser')
title_list = soup.select('div.col-times')
for i in title_list:
    title=i.select_one('div.info-movie> a > strong').text.strip()
    title_time = i.select_one(' div.info-timetable > ul > li > a > em').text.strip()
    #print(title+"의 상연시간\n"  +title_time)
    bot.sendMessage(chat_id=1180409106, text=title + "의 상영시간\n" + title_time)

#print("이상이" + time + "영화 시간표입니다.")
bot.sendMessage(chat_id=1180409106, text="이상이 " + time + "의 영화 시간표입니다.")