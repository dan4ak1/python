from bs4 import BeautifulSoup as bs
import requests
import time
with open('data.txt', encoding='utf-8') as file:
    data = file.read().split('\n')


# Авторизация на сайте ###########################
session = requests.Session()
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36'
}
url = 'https://gulayaka-edu.ru/login/index.php'
x = session.get(url).text
soup = bs(x, 'lxml')
p = soup.find(class_='mt-3').find_all('input')[1]['value']
datas = {
    'anchor': None,
    'logintoken': p,
    'username': data[1],
    'password': data[2]
}
responce = session.post(url=url, data=datas, headers=header)

# Получение списка учеников с сайта ##############
# r = session.get('https://gulayaka-edu.ru/user/index.php?id=17&perpage=500')
# main_page = r.text
# soup = bs(main_page, 'lxml')
# p = soup.find_all('th', class_="cell c1")
# names = []
# for i in range(int(len(p))):
#     if p[i].text != '' and p[i].text !=data[0]:
#         names.append(p[i].text)
#
###################################################

# Заходим на страницу с домашкой ####################
nomergr = int(input('Какую группу будем проверять?\n'))
if nomergr == 1:
    url = input('Введи ссылку на ДЗ:\n\n')
    legslo=0
    if url[-1]=='w':
        url = url + '&attempts=enrolled_with&onlygraded=0&group=3239&onlyregraded=0&slotmarks=1&tsort=timefinish&tdir=3'
        legslo=1
    elif url[-1] =='g':
        url = url + '&group=3239'
        legslo=2
    else:
        print('\nТы ввел не ту ссылку\n')
        time.sleep(5)
        exit()
if nomergr == 2:
    url = input('Введи ссылку на ДЗ:\n\n')
    legslo=0
    if url[-1]=='w':
        url = url + '&attempts=enrolled_with&onlygraded=0&group=3278&onlyregraded=0&slotmarks=1&tsort=timefinish&tdir=3'
        legslo=1
    elif url[-1] =='g':
        url = url + '&group=3278'
        legslo=2
    else:
        print('\nТы ввел не ту ссылку\n')
        time.sleep(5)
        exit()


r = session.get(url, headers=header)
soup = bs(r.text, 'lxml')
curator = soup.find(class_='usertext').text
whocanuse = ['Даниил Баландин', 'Никита Байметов', 'Даниил Каламбетов', 'Алексей Афанасенко']
if curator not in whocanuse:
    print('\n !!!!!!!!!!!!!!!!!!!!!!  У тебя нет доступа  !!!!!!!!!!!!!!!!!!!!!!\n')
    whocanuse = ''
    time.sleep(2)
    exit()
try:
    p = soup.find('div', class_='no-overflow').find('table').find('tbody').find_all('tr')
    if legslo == 1:
        maxball = float(soup.find('div', class_='no-overflow').find('table').find('thead').find(class_='header c7 bold').find('span').text.split('/')[1].split(' ')[0].replace(',', '.'))* 0.6
except AttributeError:
    print('\n!!!Ты вставил не ту ссылку, открой просмотр попыток и вставь ссылку оттуда!!!')
    time.sleep(1)
    exit()

###################################################


def download(prof_url, name):
    session = requests.Session()
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36'
    }
    url = 'https://gulayaka-edu.ru/login/index.php'
    x = session.get(url).text
    soup = bs(x, 'lxml')
    p = soup.find(class_='mt-3').find_all('input')[1]['value']
    datas = {
        'anchor': None,
        'logintoken': p,
        'username': data[1],
        'password': data[2]
    }

    responce = session.post(url=url, data=datas, headers=header)
    r = session.get(prof_url, headers=header)
    with open(name, 'wb') as file:
        file.write(r.content)


def scores():
    buff = []
    nevipoln = {}
    scores = []
    dict = {}
    if nomergr == 1:
        with open('namestable1.txt', encoding='utf-8') as file:
            namestable = file.read().split('\n')
            if '' in namestable:
                namestable.remove('')
    if nomergr == 2:
        with open('namestable2.txt', encoding='utf-8') as file:
            namestable = file.read().split('\n')
            if '' in namestable:
                namestable.remove('')
    for name in namestable:
        dict[name]=0
    s = soup.find('title')
    a = legslo
    if a == 1:
        nesdali = []
        try:
            for info in p:
                r = info.find(class_='cell c2 bold').find('a').text
                # if r in names and r not in buff and info.find(class_='cell c3').text[0:3] == 'Зав':
                if r not in buff and info.find(class_='cell c3').text[0:3] == 'Зав':

                    buff.append(r)
                    if float(info.find(class_='cell c7 bold').text.split('/')[0].replace(',', '.'))<maxball:
                        nevipoln[r] = info.find(class_='cell c7 bold').text.split('/')[0]
                    try:
                        dict[r]+=float(info.find(class_='cell c7 bold').text.split('/')[0].replace(',', '.'))
                    except KeyError as err:
                        print('\nПоправь имя в файле namestable')
                        print(r)
                        abc = input('У тебя ошибка, введи что угодно для продолжения\n')
                        time.sleep(3)
                    except NameError:
                        abc = input('У тебя ошибка, введи что угодно для продолжения\n')
                        time.sleep(3)

        except AttributeError:
            asd=123

        finally:
            print('\nТе, у кого меньше', maxball, 'баллов\n')
            for key, value in nevipoln.items():
                print(key, value)

            print('\nНе сдали тест:\n')
            for name in namestable:
                if name not in buff:
                    print(name)

            print('\n')

            for value in dict.values():
                print(str(value).replace('.', ','))

    elif a==2:

        nesdali = []

        try:
            for info in p:

                r = info.find(class_='cell c2').find('a').text
                # if r in names and r not in buff:
                if r not in buff:
                    if info.find(class_='cell c9').text[0] == '-':
                        nesdali.append(r)

                        continue
                    if info.find(class_='cell c7').text[-1] == '-':
                        continue
                    buff.append(r)
                    try:
                        print()
                        dict[r]+=float(info.find(class_='cell c7').text[6:11].replace(',', '.'))
                    except KeyError as err:
                        print('\nПоправь имя в файле namestable')
                        print(err)
                        abc = input('У тебя ошибка, введи что угодно для продолжения\n')
                        time.sleep(3)
                    except NameError:
                        abc = input('У тебя ошибка, введи что угодно для продолжения\n')
                        time.sleep(3)

        except AttributeError:
            asd=123

        finally:
            print('\nНе сдали сложку:\n')
            for name in nesdali:
                print(name)
            print('\n')
            for value in dict.values():
                print(str(value).replace('.', ','))


scores()
a = input()
