from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('https://www.naver.com/')
soup = BeautifulSoup(response, 'html.parser')
i = 1
f = open("������.txt", 'w')
for anchor in soup.select("span.ah_k"):
    data = str(i) + "�� : " + anchor.get_text() + "\n"
    i = i + 1
    f.write(data)
f.close()