#-*- coding: cp949 -*-
#-*- coding: utf-8 -*-

# 패키지
import requests
from bs4 import BeautifulSoup

# 사용자 지정 함수 만들기
def get_data(info):
    if info is None:
        return 'None'
    else:
        return info.get_text().strip()

# 크롤링 시작
df = []


# 1~5등 데이터 추출
url = f'https://www.op.gg/ranking/ladder/page=1'
resp = requests.get(url)
soup = BeautifulSoup(resp.text)

table = soup.find('div', class_='ranking-highest')
rows = table.find_all('li', class_='ranking-highest__item')

for row in rows:
    rank = get_data(row.find('div', class_='ranking-highest__rank'))
    name = get_data(row.find('a', class_='ranking-highest__name'))
    tier = get_data(row.find('div', class_='ranking-highest__tierrank').find('span'))
    lp = get_data(row.find('div', class_='ranking-highest__tierrank').find('b'))
    win = get_data(row.find('div', class_='winratio-graph__text--left'))
    lose = get_data(row.find('div', class_='winratio-graph__text--right'))
    win_ratio = get_data(row.find('span', class_='winratio__text'))
    
    # 추출한 데이터 저장
    df.append([rank, name, tier, lp, win, lose, win_ratio])


# 나머지 데이터 추출
for cur_page in range(1,4):
    url = f'https://www.op.gg/ranking/ladder/page={cur_page}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    
    # 태그 추출
    table = soup.find('table', class_='ranking-table')
    rows = table.find_all('tr', class_='ranking-table__row ')
    
    # 한 줄씩 데이터 추출
    for row in rows:
        rank = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--rank'))
        name = get_data(row.find('span'))
        tier = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--tier'))
        lp = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--lp'))
        win = get_data(row.find('div', class_='winratio-graph__text winratio-graph__text--left'))
        lose= get_data(row.find('div', class_='winratio-graph__text winratio-graph__text--right'))
        win_ratio = get_data(row.find('span', class_='winratio__text'))

        # 유저 상세 페이지 접속
        user_url = "http:" + row.find('a')['href']
        user_resp = requests.get(user_url)
        user_soup = BeautifulSoup(user_resp.text)
        
        champ_df = []
        most_champ_rows = user_soup.find_all('div', class_='ChampionBox Ranked')
        for most_champ_row in most_champ_rows[:min(3, len(most_champ_rows))]:
            champ_name = get_data(most_champ_row.find('div', class_='ChampionName').find('a'))
            champ_kda = get_data(most_champ_row.find('span', class_='KDA'))
            champ_cs = get_data(most_champ_row.find('div', title='avg. CS (CS/m)'))
            champ_win_ratio = get_data(most_champ_row.find('div', title='Win Ratio'))
            champ_num_of_play = get_data(most_champ_row.find('div', class_='Title'))
            champ_df.append([champ_name, champ_kda, champ_win_ratio, champ_num_of_play])

        # champ_df 예외처리 (예를 들어 원챔유저)
        if len(champ_df) < 3:
            gap = 3 - len(champ_df)
            for i in range(gap):
                champ_df.append(['None' for j in range(len(champ_df[0]))]) # [None, None, None, ...]

        # 추출한 데이터 저장
        df.append([rank, name, tier, lp, win, lose, win_ratio])
        print(df[-1])
