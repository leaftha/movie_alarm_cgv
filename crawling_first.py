import requests
from bs4 import BeautifulSoup

url ='http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=P013&date=20200420&screencodes=&screenratingcode=09&regioncode=103'
html = requests.get(url)
print(html.text)