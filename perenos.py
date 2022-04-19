# coding=utf-8
from bs4 import BeautifulSoup as bs
import requests
import time

# with open('data.txt', encoding='utf-8') as file:
#     data = file.read().split('\n')

data = ['Даниил Баландин', 'id182335057', 'FSB1921313131gu!']

# with open('namestable1.txt', encoding='utf-8') as file:
#     namestable1 = file.read().split('\n')
#     if '' in namestable1:
#         namestable1.remove('')
# with open('namestable2.txt', encoding='utf-8') as file:
#     namestable2 = file.read().split('\n')
#     if '' in namestable2:
#         namestable2.remove('')
# namestable = namestable1 + namestable2

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
###################################################

# r = session.get('https://gulayaka-edu.ru/mod/quiz/overrideedit.php?action=adduser&cmid=13166', headers=header)
# soup = bs(r.text, 'lxml')
#
# p = soup.find(class_='custom-select').find_all('option')
# j = 0
# dct = {}
# for i in p:
#     if i.text in namestable:
#         if i.text == 'Артём Клевров':
#             dct['Артем Алексеенко']=i.get('value')
#         elif i.text == 'Тёма Тимошенко':
#             dct['Тема Тимошенко']=i.get('value')
#         elif i.text == 'Кобзев Георгий':
#             dct['Георгий Кобзев']=i.get('value')
#         else:
#             dct[i.text]=i.get('value')
#         j+=1

dict = {'Матвей': '14729', 'Аня': '11043', 'Соня': '16401', 'Антон': '11597', 'Омар Алжанов': '18966', 'Дима Андреев': '11051', 'Арал Аскаров': '11044', 'Мария Бабкина': '11069', 'Денис Бакиев': '19009', 'Диана Вербина': '18985', 'Данил Вернандский': '19510', 'Полина Водопьянова': '11347', 'Дарья Габдрахманова': '18984', 'Влад Гельцер': '11055', 'Георгий Кобзев': '13297', 'Булат Гимаев': '18981', 'Василий Горбань': '11210', 'Полина Долгополова': '15286', 'Максим Жиляев': '11067', 'Артур Зарецкий': '12077', 'Настя Здравствуй': '10933', 'Максим Зеленский': '11346', 'Макс Иваненко': '11890', 'Владислав Иванов': '19355', 'Ставр Иванов': '17873', 'Дарья Иванова': '11049', 'Дмитрий Казаков': '15283', 'Сергей Капустин': '11058', 'Искандер Кильдин': '11059', 'Артем Алексеенко': '11057', 'Макс Князев': '19490', 'Иван Комаров': '11190', 'Ирина Кречетова': '11048', 'Виолетта Кузнецова': '13798', 'Дарья Кузовова': '11064', 'Олег Куркин': '11356', 'Екатерина Лазарева': '11362', 'Родион Марков': '14626', 'Алексей Мелешин': '11361', 'Дарья Минко': '11040', 'Ярослав Митрофанов': '11675', 'Настя Митрофанова': '18983', 'Дарья Оборотова': '11068', 'Миша Осипов': '11047', 'Никита Петров': '11046', 'Дарина Подборнова': '11060', 'Антон Попов': '11041', 'Никита Потякин': '19356', 'Валера Романов': '11050', 'Дарья Сиденко': '13519', 'Иван Сорокин': '19303', 'Мурад Тайгибов': '18979', 'Дарья Тарадова': '19304', 'Тема Тимошенко': '11056', 'Вадим Ткаченко': '11053', 'Илья Ткаченко': '11061', 'Тимофей Трапицын': '11194', 'Алина Ужевская': '18980', 'Айгуль Учар': '12070', 'Вова Ханоян': '11205', 'Каролина Хачатурова': '11340', 'Илья Циммерман': '11052', 'Никита Шалаев': '18739', 'Даниил Шутов': '11343', 'Матвей Щеглов': '11208', 'Арсений Яковлев': '11199', 'Камилла Янбулатова': '19953'}


sesskey = ''


def linkss(n):
    global sesskey
    url = 'https://gulayaka-edu.ru/course/view.php?id=112&section=' + str(n)

    r = session.get('https://gulayaka-edu.ru/course/view.php?id=112', headers=header)
    main_page = r.text
    soup = bs(main_page, 'lxml')
    p = soup.find_all(class_='dropdown-item menu-action')
    sesskey = p[-1].get('href').split('=')[-1]
    r = session.get(url, headers=header)
    main_page = r.text
    soup = bs(main_page, 'lxml')

    p = soup.find_all(class_='activityinstance')
    for link in p:
        if 'quiz' in str(link.find('a').get('href')) or 'assign' in str(link.find('a').get('href')):
            links.append(link.find('a').get('href'))

    if int(len(links)) > 2:
        del links[-1]


def resp(name):
    try:
        for link in links:

            id = link.split('=')[1]
            if 'quiz' in str(link):
                name1 = 'quiz'
                datas = {
                    'action': 'adduser',
                    'cmid': id,
                    'sesskey': sesskey,
                    '_qf__quiz_override_form': 1,
                    'mform_isexpanded_id_override': 1,
                    'userid': dict[name],
                    'password': '',
                    'attempts': 0,
                    'submitbutton': 'Сохранить'
                }
            else:
                name1 = 'assign'
                datas = {
                    'action': 'adduser',
                    'cmid': id,
                    'sesskey': sesskey,
                    '_qf__assign_override_form': 1,
                    'mform_isexpanded_id_override': 1,
                    'userid': dict[name],
                    'submitbutton': 'Сохранить'
                }

            responce = session.post(url=f'https://gulayaka-edu.ru/mod/{name1}/overrideedit.php', data=datas, headers=header)
        print('ЗАЕБИСЬ\n')
    except KeyError:
        print('УПИЗДОК\n')


n = int(input('Введи n:  '))
n = 110 - n
while 1:
    links1 = []
    name = input('Введи имя:  ')

    try:
        name = int(name)
        n = 110 - name
        print('==========НОВАЯ ДОМАШКА==========\n')
    except ValueError:
        linkss(n)
        resp(name)
