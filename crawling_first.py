import requests
from bs4 import BeatifulSoup

url ='http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?theatercode=P013&screencodes=&screenratingcode=09&regioncode=103'
html = requests.get(url)
print(html.text)