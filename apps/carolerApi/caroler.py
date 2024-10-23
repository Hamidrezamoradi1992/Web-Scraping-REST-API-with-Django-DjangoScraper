from pprint import pprint

from bs4 import BeautifulSoup
import requests

MONT = {'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4, 'مرداد': 5, 'شهریور': 6, 'مهر': 7, 'آبان': 8, 'آذر': 9,
        'دی': 10, 'بهمن': 1, 'اسفند': 12}
url = 'https://www.teh-music.com/music/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
pages = soup.find('ul', {'class': 'page-numbers'}).find_all('li')
last_page = 10 if 10 < (c := int(pages[len(pages) - 2].find('a').get('href').split('/')[-2])) else c
list_url_music = []
for i in range(1, last_page + 1):
    url = 'https://www.teh-music.com/music/page/{}/'.format(i)
    response = requests.get(url)
    soup2 = BeautifulSoup(response.content, 'html.parser')
    list_item_in_page = soup2.find('article').find('div', {'class': 'new_music'}).find('div',
                                                                                       {'class': 'list'}).find_all(
        'div', {'class': 'item'})
    list_url_music += [i.find('div', {'class': 'poster'}).find('a').get('href') for i in list_item_in_page]
    print('page {}'.format(i))

pprint(list_url_music)
for i in list_url_music:
    response = requests.get(i)
    soup_detail_music = BeautifulSoup(response.content, 'html.parser')
    # body > main > div.top > div.left_side.fr > div.up > article > section > p:nth-child(3)
    title_music = \
        soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {'class': 'left_side'}).find('div', {
            'class': 'up'}).find('article').find('section').find_all('p')[0].get_text().split('به نام ')[1]
    # body > main > div.top > div.left_side.fr > div.up > article > div.singer > a
    actor = (soup_detail_music.find('main').find('div', {'class': 'top'}).
             find('div', {'class': 'left_side'}).find('div', {'class': 'up'}).find(
        'article').find('div', {'class': 'singer'}).find('a').get_text())
    # body > main > div.top > div.left_side.fr > div.down > div.stat > div: nth - child(3) > i
    time = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {
        'class': 'left_side'}).find('div', {'class': 'down'}).find(
        'div', {'class': 'stat'}).childGenerator()
    # body > main > div.top > div.left_side.fr > div.down > div.stat > div.item.categorys > a: nth - child(4)
    category = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {'class': 'left_side'}).find(
        'div', {
            'class': 'down'}).find('div', {'class': 'stat'}).find('div', {'class': 'categorys'}).get_text()
    # body > main > div.top > div.left_side.fr > div.down > div.dlbox.add_dl.end > div: nth - child(1) > a
    link_download = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div',
                                                                                      {'class': 'left_side'}).find(
        'div', {
            'class': 'down'}).find('div', {'class': 'add_dl'}).find_all('a')
    # body > main > div.top > div.poster.fr > a > figure > img
    cover_music = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {'class': 'poster'}).find(
        'img').get('src').split(' ')
    link_downloads = []
    for i in link_download:
        s = i.get('href').split(" ")
        link_downloads.append(str.join('%20', s))

    print(category.strip().split(','))
    print(list(zip([link for link in link_downloads], [link.get('title').split(" ")[4] for link in link_download])))
    print(str.join("%20",cover_music))
    print(title_music)
    print(actor)
    times = list(time)[5].get_text().split('\n\n\t\t\t\t\t\t\t')[1].split('\t\t\t\t\t\t')[0].split(' ')
    for k, vv in MONT.items():
        if times[1] == k:
            times[1] = vv
    print(times)
    print('\n' * 3)

# print(soup.find('div',attrs={'class':'mf_rw'}).find('main').find('div').find('article').get('data-artist',None))
# soup.find('div',attrs={'class':'mf_rw'}).find('main').find('div').find('article')
# all_class = soup.find('div',attrs={'class':'mf_rw'}).find('main').find('div').find_all('article',{'class':'mf_pst'})
# body > div.mf_rw > main > div > article:nth-child(2)
# print((soup.find('div',attrs={'class':'mf_rw'}).find('main').find('div').find('article').find('header').find('h2').find('a').get('href',None)))
# for s in all_class:

# print(s.get('data-artist',None))
# print(s.find('header').find('h2').find('a').get('href',None))
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
# driver.get("https://python.org")
# print(driver.)
# driver.close()
