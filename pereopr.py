from bs4 import BeautifulSoup as bs
import requests


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
###################################################
print('SSSTARTTT')
j=1
for i in range(1, 41):
    r = session.get(f'https://gulayaka-edu.ru/course/view.php?id=17&section={i}&singlesec={i}', headers=header)
    main_page = r.text
    soup = bs(main_page, 'lxml')
    p = soup.find_all(class_='activityinstance')
    links = []
    for link in p:
        if 'quiz' in str(link.find('a').get('href')) or 'assign' in str(link.find('a').get('href')):
            links.append(link.find('a').get('href'))

    for link in links:
        id = link.split('=')[1]
        if 'quiz' in str(link):
            name = 'quiz'
        else:
            name = 'assign'
        print(id, name)
        r = session.get(f'https://gulayaka-edu.ru/mod/{name}/overrides.php?cmid={id}&mode=user', headers=header)
        main_page = r.text
        soup = bs(main_page, 'lxml')
        if name == 'quiz':
            p = soup.find_all(class_='colaction cell c4 lastcol')
        else:
            p = soup.find_all(class_='colaction cell c3 lastcol')
        lidel = []
        for i in p:
            lidel.append(i.find_all('a')[2].get('href'))

        for li in lidel:
            a = li.split('?')[1].split('&')
            id = a[0].replace('id=', '')
            sesskey = a[1].replace('sesskey=', '')
            print(j)
            j+=1
            datas = {
                'id': id,
                'confirm': 1,
                'sesskey': sesskey
            }
            responce = session.post(url=f'https://gulayaka-edu.ru/mod/{name}/overridedelete.php', data=datas, headers=header)
###################################################
