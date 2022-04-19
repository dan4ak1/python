from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import os

with open('datavk.txt', encoding='utf-8') as file:
    datavk = file.read().split('\n')

with open('links.txt', encoding='utf-8') as file:
    links = file.read().split('\n')

with open('cost.txt', encoding='utf-8') as file:
    costs = file.read().split('\n')

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path=f"{os.getcwd()}\\chromedriver.exe",
    options=options
)
url = 'https://vk.com/'
driver.get(url)
login = driver.find_element_by_id('index_email')
password = driver.find_element_by_id('index_pass')
time.sleep(1)
login.send_keys(datavk[0])
time.sleep(1)
password.send_keys(datavk[1])
time.sleep(1)
password.send_keys(Keys.ENTER)
time.sleep(2)
i=0
for link in links:
    driver.get(link)
    time.sleep(2)
    try:
        close = driver.find_element_by_class_name('box_x_button').click()
    except NoSuchElementException:
        b=1
    time.sleep(3)
    page = driver.page_source
    soup = bs(page, 'lxml')
    name = soup.find(class_="page_name").text.split(' ')[0]
    if name == 'Krvsky':
        name = 'Аня'

    if name == 'Anton':
        name = 'Антон'

    if name == 'Matvey':
        name = 'Матвей'

    a = f''' Привет, {name} \n
    1) Нужно оценить мою работу в этом месяце, вот форма для оценки, сделай все
    Пора платить по счетам, поэтому вот тебе ссылочбка для оплаты:
    https://ebonit100.ru/pay22 \n
    Оплатить нужно {costs[i]}, срок оплаты - до 30 января, но ты можешь попросить у меня отсрочку до 5 февраля максимум \n
    Ну и ссылка на твою страницу, вставь ее при оплате: {link}'''
    time.sleep(1)
    message = driver.find_element_by_class_name('FlatButton__content').click()
    time.sleep(1)
    print1 = driver.find_element_by_id('mail_box_editable').send_keys(a)
    time.sleep(1)
    enter = driver.find_element_by_id('mail_box_send').click()
    i+=1
