import requests
from bs4 import BeautifulSoup
from datetime import datetime

toyear = str(datetime.today().year)
tomonth = str(datetime.today().month)
today = str(datetime.today().day)
time = str(toyear + tomonth + today)
url = 'http://www.cgv.co.kr//common/showtimes/iframeTheater.aspx?areacode=05,207&theatercode=0005&date='+time
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
title_list = soup.select('div.col-times')
for i in title_list:
    title = i.select_one('div.info-movie> a > strong').text.strip()
    title_time = i.select_one('  div.sect-showtimes > div.info-timetable > ul > li')
    print(title + "의 상영시간\n")
    for a in title_list:
        times = a.select_one('a > em').text.strip()
        print(times)

print("이상이 " + time + "의 영화 시간표입니다")