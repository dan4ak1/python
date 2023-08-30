from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import datetime
import portion as p


def log(login1, password1):
    url = 'https://csgo3.run/'
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_class_name('agree-switcher__text').click()
    time.sleep(1)
    driver.find_element_by_class_name('hide-below-m').click()
    time.sleep(3.5)
    data = driver.find_elements_by_class_name('newlogindialog_TextInput_2eKVn')
    login = data[0]
    password = data[1]
    time.sleep(0.5)
    login.send_keys(login1)
    time.sleep(0.2)
    password.send_keys(password1)
    time.sleep(0.2)
    password.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.find_element_by_class_name('btn_green_white_innerfade').click()
    time.sleep(4)


def buy(price):
    price = str(price)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(74, 846).click().perform()
    time.sleep(0.1)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(87, 542).click().perform()
    time.sleep(0.1)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(857, 426).click().perform()
    ActionChains(driver).send_keys(price).perform()
    time.sleep(0.1)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(554, 518).click().perform()
    time.sleep(0.1)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(835, 357).click().perform()
    time.sleep(0.1)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(905, 277).click().perform()
    time.sleep(0.3)


def stavka(kf):
    kf = str(kf)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1056, 229).click().perform()
    time.sleep(0.1)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1100, 279).double_click().perform()
    time.sleep(0.1)
    ActionChains(driver).send_keys(kf).perform()
    time.sleep(0.1)


def pognal():
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1341, 279).click().perform()
    time.sleep(0.5)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1341, 279).click().perform()
    time.sleep(0.5)
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1341, 279).click().perform()


def select():
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(87, 542).click().perform()
    time.sleep(0.2)


def info(dic):
    for sl in slot:
        dic[int(sl.get('href').split('/')[-1])] = float(sl.text[0:-1])
    dic = dict(sorted(dic.items()))
    print(dic)
    time.sleep(300)


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(
    executable_path=f"{os.getcwd()}\\chromedriver.exe",
    options=options
)
driver.set_window_size(1920, 1080)
url = 'https://csgo3.run/'
driver.get(url)

with open('data.txt', encoding='utf-8') as file:
    data = file.read().split('\n')

log(str(data[0]), str(data[1]))
price = str(data[2])
print(price)
buy(float(price))
stt = float(data[3])
stavka(stt)
x = {}
bank0 = int(data[5])
print(bank0)
raz = int(data[4])
check = 0
xx1 = []
r1 = p.open(float(price) * 0.95, float(price) * 1.05)
print(r1)
flag = 1
bank1 = 25
starttime = time.time()
while 1:
    k = 0
    z = 0
    check = 0
    page = driver.page_source
    soup = bs(page, 'lxml')
    start = soup.find(class_="graph-svg countdown")
    slot = soup.find_all(
        class_="h-35 md:h-40 min-w-50 md:min-w-60 px-7 shrink-0 grid place-content-center border-t-2 transition "
               "hover:brightness-110")
    try:
        bank = float(soup.find(class_='header-user__balance').text[0:-1])
    except AttributeError:
        z = False
        time.sleep(1)
        driver.get(url)
        time.sleep(2)
        stavka(stt)
        time.sleep(1)

    if bank < bank0:
        flag = 0
    if bank > bank1:
        flag = 0

    xx = slot[0:10]

    try:
        for i in range(10):
            xx[i] = float(xx[i].text[0:-1])
        z = all([x < stt for x in xx[0:raz]])
    except IndexError:
        z = False
        time.sleep(1)
        driver.get(url)
        time.sleep(2)
        stavka(stt)
        time.sleep(1)

    if (flag == 1) and ('checked' in str(soup.find(class_='grid place-content-start gap-6 '
                                                          'lg:gap-9 grid-cols-3 '
                                                          'sm:grid-fill-120'))):
        select()

    if (flag == 1) and (xx1 != xx) and ('button' not in str(soup.find(class_='grid place-content-start gap-6 '
                                                                             'lg:gap-9 grid-cols-3 '
                                                                             'sm:grid-fill-120'))):
        buy(float(price))
    a = str(soup.find(class_='grid place-content-start gap-6 '
                             'lg:gap-9 grid-cols-3 '
                             'sm:grid-fill-120'))

    try:
        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.66:
            flag = 0
            time.sleep(1)
        if str(0.88) in a:
            z = False
            time.sleep(1)
            driver.get(url)
            time.sleep(2)
            stavka(stt)
            time.sleep(2)
            buy(float(price))
        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.77:
            endtime = time.time()
            starttime = time.time()
            print(endtime - starttime)
            flag = 1
            time.sleep(1)
        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.22:
            time.sleep(15)
            page = driver.page_source
            soup = bs(page, 'lxml')
            a = str(soup.find(class_='grid place-content-start gap-6 '
                                     'lg:gap-9 grid-cols-3 '
                                     'sm:grid-fill-120'))
            bank0 = int(float(a[a.find('price') + 7:a.find('$') - 1])*100)
            print('bank0', bank0)
            time.sleep(1)

        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.33:
            time.sleep(15)
            page = driver.page_source
            soup = bs(page, 'lxml')
            a = str(soup.find(class_='grid place-content-start gap-6 '
                                     'lg:gap-9 grid-cols-3 '
                                     'sm:grid-fill-120'))
            bank1 = int(float(a[a.find('price') + 7:a.find('$') - 1]) * 100)
            print('bank1', bank1)
            time.sleep(1)

        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.44:
            time.sleep(10)
            page = driver.page_source
            soup = bs(page, 'lxml')
            a = str(soup.find(class_='grid place-content-start gap-6 '
                                     'lg:gap-9 grid-cols-3 '
                                     'sm:grid-fill-120'))
            stt = float(a[a.find('price') + 7:a.find('$') - 1])

            print('STAVKA =', stt)
            stavka(stt)
            time.sleep(1)

        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.55:
            time.sleep(10)
            page = driver.page_source
            soup = bs(page, 'lxml')
            a = str(soup.find(class_='grid place-content-start gap-6 '
                                     'lg:gap-9 grid-cols-3 '
                                     'sm:grid-fill-120'))
            raz = int(round(float(a[a.find('price') + 7:a.find('$') - 1])))
            print('RAZ =', raz)

        if float(a[a.find('price') + 7:a.find('$') - 1]) == 0.99:
            # price = str(round((float(price) + 0.10), 2)) + '0'
            # print('price =', price)
            time.sleep(10)
            page = driver.page_source
            soup = bs(page, 'lxml')
            a = str(soup.find(class_='grid place-content-start gap-6 '
                                     'lg:gap-9 grid-cols-3 '
                                     'sm:grid-fill-120'))
            price = str(float(a[a.find('price') + 7:a.find('$') - 1])) + '0'
            print('price =', price)
            r1 = p.open(float(price) * 0.95, float(price) * 1.05)
            print(r1)
            time.sleep(1)
        res = float(a[a.find('price') + 7:a.find('$') - 1]) in r1
    except:
        res = True

    # print('flag =', flag)
    # print('z =', z)
    if (res is False) and (flag == 1):
        if 'price' in a:
            buy(float(price))

    if (start is None) or (z is False) or (flag == 0):

        k = 0
    else:
        k = 1
    if k == 1:
        endtime = time.time()
        if endtime - starttime > 20000:
            flag = 0
        select()
        while 1:
            page1 = driver.page_source
            soup1 = bs(page1, 'lxml')
            butt1 = soup1.find(class_='input-base text-[#dbe1f8]')
            start1 = soup1.find(class_="graph-svg countdown")
            if start1 is None:
                if check == 0:
                    select()
                break

            if 'disabled' in str(butt1):
                check = 1
                slot1 = soup1.find_all(
                    class_="h-35 md:h-40 min-w-50 md:min-w-60 px-7 shrink-0 grid place-content-center border-t-2 "
                           "transition "
                           "hover:brightness-110")
                xx1 = slot1[0:10]
                for i in range(10):
                    xx1[i] = float(xx1[i].text[0:-1])
                break
            pognal()
