#-*- coding: cp949 -*-
#-*- coding: utf-8 -*-


import urllib.request
from bs4 import BeautifulSoup
import csv

hdr = { 'User-Agent' : 'Mozilla/5.0' }
url = 'https://www.melon.com/chart/index.htm'

req = urllib.request.Request(url, headers= hdr)
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html,'html.parser')


lst50 = soup.select('.lst50,.lst100')

for i in lst50:
    print(i.select_one('.rank').text, end ='위 ')
    print(i.select_one('.ellipsis.rank01').a.text, end = ' ')
    print(i.select_one('.ellipsis.rank02').a.text, end = ' ')
    print(i.select_one('.ellipsis.rank03').a.text)
