#!python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
import time

from pymongo import MongoClient

# ============= Mongo ==============
mongo_username = 'admin'
mongo_password = 'admin'
mongo_client = MongoClient('mongodb://%s:%s@127.0.0.1' % (mongo_username, mongo_password))
# Указатель на базу данных, может быть множество
mongo_db = mongo_client['emails']

stat = {
    'saved': 0,
    'unsaved': 0,
}

# ============ Selenium ============
options = Options()
options.add_argument('--window-size=1900,1000')

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(10)

driver.get('https://mail.ru')

# Login
login_form = driver.find_element(By.CLASS_NAME, 'email-input')
login_form.click()
login_form.send_keys('study.ai_172')
driver.find_element(By.XPATH, '//button[@data-testid="enter-password"]').click()

# Password
pw_form = driver.find_element(By.XPATH, '//input[@data-testid="password-input"]')
pw_form.click()
pw_form.send_keys('NextPassword172#')

driver.find_element(By.XPATH, '//button[@data-testid="login-to-mail"]').click()

page = driver.find_elements(By.XPATH, '//a[contains(@href, "/inbox/0:")]')

mail_id = set()


def get_mails():
    page = driver.find_elements(By.XPATH, '//a[contains(@href, "/inbox/0:")]')
    for i in page:
        href = i.get_attribute('href')
        # id = href.split(":")[2]
        # print(id)
        mail_id.add(href)
    print(len(mail_id))


def push_down(count):
    s = 0
    for i in range(count):
        count = len(mail_id)
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN)
        actions.perform()
        s = s + 1
        print(s)
        time.sleep(0.2)
        get_mails()
        if len(mail_id) > count:
            time.sleep(0.5)


def mail_detail(mail_set):
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[-1])
    mail_List = []
    for i in mail_set:
        m = {}
        driver.get(i)
        head = driver.find_element(By.CLASS_NAME, 'letter__header-row')
        sender = head.find_element(By.CLASS_NAME, 'letter-contact').get_attribute('title')
        date = head.find_element(By.CLASS_NAME, 'letter__date').text
        subject = driver.find_element(By.CLASS_NAME, 'thread__subject').text

        body = driver.find_element(By.XPATH, "//div[@class='letter__body']").text

        print(sender, date, subject, )
        m.update({
            'sender': sender,
            'date': date,
            'subject': subject,
            'body': body,
            'href': i,
        })
        mail_List.append(m)
    return mail_List


def to_mongo(json):
    """
    Функция записи данных в БД
    :param json:
    :return:
    """

    if not mongo_db['hot_news'].count_documents({'href': json['href']}) > 0:
        mongo_db['hot_news'].insert_one(json)
        print("=== Новое письмо сохранено в БД\n")
        stat['saved'] += 1
    else:
        print('=== Письмо уже содежиться в БД\n')
        stat['unsaved'] += 1


get_mails()
push_down(40)
data = mail_detail(mail_id)
print('Test')
for mail in data:
    to_mongo(mail)


if __name__ == "__main__":
    pass
