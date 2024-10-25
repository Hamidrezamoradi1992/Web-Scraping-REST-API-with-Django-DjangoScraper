from selenium.webdriver.common.by import By
from time import sleep

from selenium.webdriver.common.keys import Keys

from .models import Category, Music
from pprint import pprint
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def new_music_caroler(ur=None):
    MONT = {'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4, 'مرداد': 5, 'شهریور': 6, 'مهر': 7, 'آبان': 8,
            'آذر': 9,
            'دی': 10, 'بهمن': 1, 'اسفند': 12}
    url = 'https://www.teh-music.com/music/' if ur is None else ur
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages = soup.find('ul', {'class': 'page-numbers'}).find_all('li')
    last_page = 10 if 10 < (c := int(pages[len(pages) - 2].find('a').get('href').split('/')[-2])) else c
    list_url_music = []
    # , last_page + 1
    for i in range(1, last_page + 1):
        url = 'https://www.teh-music.com/music/page/{}/'.format(i)
        response = requests.get(url)
        soup2 = BeautifulSoup(response.content, 'html.parser')
        list_item_in_page = soup2.find('article').find('div', {'class': 'new_music'}).find('div',
                                                                                           {'class': 'list'}).find_all(
            'div', {'class': 'item'})
        list_url_music += [i.find('div', {'class': 'poster'}).find('a').get('href') for i in list_item_in_page]
        print('page {}'.format(i))

    database_url_music = [i[0] for i in Music.objects.all().values_list('url_detail_page')]
    for urls in list_url_music:
        if urls not in database_url_music:
            response = requests.get(urls)
            soup_detail_music = BeautifulSoup(response.content, 'html.parser')
            # body > main > div.top > div.left_side.fr > div.up > article > section > p:nth-child(3)
            title_music = \
                soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {'class': 'left_side'}).find(
                    'div',
                    {
                        'class': 'up'}).find(
                    'article').find('section').find_all('p')[0].get_text().split('به نام ')[1]
            # body > main > div.top > div.left_side.fr > div.up > article > div.singer > a
            actor = (soup_detail_music.find('main').find('div', {'class': 'top'}).
                     find('div', {'class': 'left_side'}).find('div', {'class': 'up'}).find(
                'article').find('div', {'class': 'singer'}).find('a').get_text())
            # body > main > div.top > div.left_side.fr > div.down > div.stat > div: nth - child(3) > i
            time = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {
                'class': 'left_side'}).find('div', {'class': 'down'}).find(
                'div', {'class': 'stat'}).childGenerator()
            # body > main > div.top > div.left_side.fr > div.down > div.stat > div.item.categorys > a: nth - child(4)
            category = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div',
                                                                                         {'class': 'left_side'}).find(
                'div', {
                    'class': 'down'}).find('div', {'class': 'stat'}).find('div', {'class': 'categorys'}).get_text()
            # body > main > div.top > div.left_side.fr > div.down > div.dlbox.add_dl.end > div: nth - child(1) > a
            link_download = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div',
                                                                                              {
                                                                                                  'class': 'left_side'}).find(
                'div', {
                    'class': 'down'}).find('div', {'class': 'add_dl'}).find_all('a')
            # body > main > div.top > div.poster.fr > a > figure > img
            cover_music = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div',
                                                                                            {'class': 'poster'}).find(
                'img').get('src').split(' ')
            link_downloads = []
            for i in link_download:
                s = i.get('href').split(" ")
                link_downloads.append(str.join('%20', s))
            list_cat = [i.strip() for i in category.strip().split('،')]
            for categories in list_cat[1::]:
                try:
                    Category.objects.create(title=categories.strip())
                except Exception as e:
                    print(e)
            list_cat2 = Category.objects.filter(title__in=list_cat[1::])
            url_downloads = (dict(zip([int(link.get('title').split(" ")[4]) for link in link_download],
                                      [link for link in link_downloads])))
            cover = str.join("%20", cover_music)

            # print(title_music)
            # print(actor)
            # print(urls)
            try:
                m = Music.objects.create(title_music=title_music, actor_name=actor, url_detail_page=urls,
                                         url_picture=cover, link_downloads_128=url_downloads[128],
                                         link_downloads_300=url_downloads[320])
                m.music_category.add(*list_cat2)
                m.save()
            except Exception as e:
                print(e)

            times = list(time)[5].get_text().split('\n\n\t\t\t\t\t\t\t')[1].split('\t\t\t\t\t\t')[0].split(' ')
            for k, vv in MONT.items():
                if times[1] == k:
                    times[1] = vv
            # print(times)
            # print('\n' * 3)


def searchmusic(title):
    MONT = {'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4, 'مرداد': 5, 'شهریور': 6, 'مهر': 7, 'آبان': 8,
            'آذر': 9,
            'دی': 10, 'بهمن': 1, 'اسفند': 12}
    title_music = ''
    list_tracks = ''
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.teh-music.com/")
    driver.find_element(By.XPATH, '/html/body/header/div[2]/div/form/input[1]').send_keys(title)
    driver.find_element(By.XPATH, '/html/body/header/div[2]/div/form/input[2]').send_keys(Keys.ENTER)
    sleep(2)
    url = driver.current_url
    sleep(5)
    driver.close()

    list_url_music = []
    response = requests.get(url)
    soup2 = BeautifulSoup(response.content, 'html.parser')
    try:
        list_item_in_page = soup2.find('article').find('div', {'class': 'new_music'}).find('div',
                                                                                           {'class': 'list'}).find_all(
            'div', {'class': 'item'})
        list_url_music += [i.find('div', {'class': 'poster'}).find('a').get('href') for i in list_item_in_page]
    except AttributeError:
        return False
    database_url_music = [i[0] for i in Music.objects.all().values_list('url_detail_page')]
    for urls in list_url_music:
        if urls not in database_url_music:
            response = requests.get(urls)
            print(urls)
            soup_detail_music = BeautifulSoup(response.content, 'html.parser')
            soup_album = soup_detail_music.find('div', {'class': 'tracks'})
            if soup_album is None:
                try:
                    # body > main > div.top > div.left_side.fr > div.up > article > section > p:nth-child(3)
                    title_music = soup_detail_music.find(
                        'main').find(
                        'div', {'class': 'top'}).find(
                        'div', {'class': 'left_side'}).find(
                        'div', {'class': 'up'}).find('article').find(
                        'section').find_all(
                        'p')[0].get_text().split('به نام ')[1]
                    # body > main > div.top > div.left_side.fr > div.up > article > div.singer > a
                    actor = (soup_detail_music.find(
                        'main').find('div', {'class': 'top'}).
                             find('div', {'class': 'left_side'}
                                  ).find('div', {'class': 'up'}).find('article'
                                                                      ).find('div', {'class': 'singer'}
                                                                             ).find('a').get_text())
                    # # body > main > div.top > div.left_side.fr > div.down > div.stat > div: nth - child(3) > i
                    # time = soup_detail_music.find('main').find('div', {'class': 'top'}).find('div', {
                    #     'class': 'left_side'}).find('div', {'class': 'down'}).find(
                    #     'div', {'class': 'stat'}).childGenerator()

                    category = soup_detail_music.find(
                        'main').find(
                        'div', {'class': 'top'}).find(
                        'div', {'class': 'left_side'}).find(
                        'div', {'class': 'down'}).find(
                        'div', {'class': 'stat'}).find(
                        'div', {'class': 'categorys'}).get_text()
                    # body > main > div.top > div.left_side.fr > div.down > div.dlbox.add_dl.end > div: nth - child(1) > a
                    link_download = soup_detail_music.find('main').find(
                        'div', {'class': 'top'}).find(
                        'div', {'class': 'left_side'}).find(
                        'div', {'class': 'down'}).find(
                        'div', {'class': 'add_dl'}).find_all('a')
                    # body > main > div.top > div.poster.fr > a > figure > img
                    cover_music = soup_detail_music.find('main'
                                                         ).find('div', {'class': 'top'}
                                                                ).find('div', {'class': 'poster'}
                                                                       ).find('img').get('src').split(' ')
                except Exception as e:
                    print('11111', e)
                    return False

                link_downloads = []
                for i in link_download:
                    s = i.get('href').split(" ")
                    link_downloads.append(str.join('%20', s))
                list_cat = [i.strip() for i in category.strip().split('،')]
                for categories in list_cat[1::]:
                    try:
                        Category.objects.create(title=categories.strip())
                    except Exception as e:
                        print(e)
                list_cat2 = Category.objects.filter(title__in=list_cat[1::])
                url_downloads = (dict(zip([int(link.get('title').split(" ")[4]) for link in link_download],
                                          [link for link in link_downloads])))
                cover = str.join("%20", cover_music)

                # print(title_music)
                # print(actor)
                # print(urls)
                try:
                    m = Music.objects.create(title_music=title_music, actor_name=actor, url_detail_page=urls,
                                             url_picture=cover, link_downloads_128=url_downloads[128],
                                             link_downloads_300=url_downloads[320])
                    m.music_category.add(*list_cat2)
                    m.save()
                except Exception as e:
                    print(e)
                return True

            else:

                try:

                    # body > main > div.top > div.left_side.fr > div.down > div.stat > div: nth - child(1) > a
                    category = soup_detail_music.find(
                        'main').find(
                        'div', {'class': 'top'}).find(
                        'div', {'class': 'left_side'}).find(
                        'div', {'class': 'down'}).find(
                        'div', {'class': 'stat'}).find(
                        'div', {'class': 'item'}).find(
                        'a').get_text()

                    cover_music = soup_detail_music.find('main'
                                                         ).find('div', {'class': 'top'}
                                                                ).find('div', {'class': 'poster'}
                                                                       ).find('img').get('src').split(' ')
                    # body > main > div.top > div.left_side.fr > div.up > article > div.singer
                    actor = (soup_detail_music.find(
                        'main').find('div', {'class': 'top'}).
                             find('div', {'class': 'left_side'}
                                  ).find('div', {'class': 'up'}).find('article'
                                                                      ).find('div', {'class': 'singer'}
                                                                             ).get_text())

                    # body > main > div.album - player > div.tracks
                    list_tracks = soup_detail_music.find(
                        'div', {'class': 'album-player'}).find(
                        'div', {'class': 'tracks'}).find_all(
                        'div', {'class': 'item'})
                except Exception as e:
                    print(e)
                    return False

            list_cat = [i.strip() for i in category.strip().split('،')] if len(category.strip().split('،')) > 1 else [
                category.strip()]
            for categories in list_cat:
                try:
                    Category.objects.create(title=categories.strip())
                except Exception as e:
                    print(e)
            for i in list_tracks:
                link_download = [d.find('a') for d in i.find_all('div', {'class': 'dl'})]
                print('link_download', link_download)
                title_music = i.find('div', {'class': 'name'}).get_text()
                link_downloads = []
                for i in link_download:
                    s = i.get('href').split(" ")
                    link_downloads.append(str.join('%20', s))
                list_cat2 = Category.objects.filter(title__in=list_cat)
                url_downloads = (dict(zip([128, 320], [link for link in link_downloads])))
                cover = str.join("%20", cover_music)
                urls += "1"
                try:
                    m = Music.objects.create(title_music=title_music, actor_name=actor, url_detail_page=urls,
                                             url_picture=cover, link_downloads_128=url_downloads[128],
                                             link_downloads_300=url_downloads[320])
                    m.music_category.add(*list_cat2)
                    m.save()
                    print('hamid')
                except Exception as e:
                    print(e)
            else:
                return True
                # times = list(time)[5].get_text().split('\n\n\t\t\t\t\t\t\t')[1].split('\t\t\t\t\t\t')[0].split(' ')
                # for k, vv in MONT.items():
                #     if times[1] == k:
                #         times[1] = vv
        # print(times)
        # print('\n' * 3)

    return False
