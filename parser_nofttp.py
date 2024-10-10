import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import json
import time
import random

import zipfile

from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Создание папки json-s, если она не существует
# if not os.path.exists('json-s'):
#     os.makedirs('json-s')

# Список сайтов
websites = ['1.2.com',
'niistekla.ru',
'osz-glass.ru',
'km-meat.ru',
'tonnel2001.ru',
'surgut-rsu.ru']

# Список прокси-серверов
proxy_list = [
    "194.67.216.69:9371"]

# Логин и пароль для прокси
proxy_auth = "mu0VkE:jjVMqA"


# Список для хранения данных о каждом сайте
websites_data = []

# Указание пути к драйверу и создание объекта options
service = Service(executable_path='C:\\Users\\chromedriver.exe')
options = webdriver.ChromeOptions()

# Запуск браузера с использованием прокси
driver = webdriver.Chrome(service=service, options=options)


def get_next_proxy():
    if proxy_list:
        proxy = proxy_list.pop(0)
        
        options = webdriver.ChromeOptions()
        proxy_auth_extension = "--proxy-server=" + proxy
        options.add_argument(proxy_auth_extension)
        
        return options
    else:
        print("Ran out of proxies!")
        return None


# Счетчик посещенных сайтов и счетчик прокси
visited_count = 0
proxy_count = 0

# Цикл для обработки каждого сайта
for website in websites:

#if visited_count > 0 and visited_count % 1 == 0:
# Получение следующего прокси из списка
    options = get_next_proxy()
    if options:
        driver.quit()

        driver = webdriver.Chrome(service=service, options=options)
    #     proxy_count += 1
    # else:
    #     break


# Получение текущего сайта из списка
    website_url = website

    # Переход на сайт dnsdumpster.com
    driver.get("https://dnsdumpster.com/")

    # Ждем пока поле поиска станет доступным
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "targetip")))

    # Очистка поля ввода и ввод значения
    search_box.clear()
    search_box.send_keys(website_url)
    search_box.send_keys(Keys.RETURN)

    # Ожидание загрузки результатов поиска
    driver.implicitly_wait(10)

    # Получение HTML-кода страницы
    html_code = driver.page_source

    # Сохранение данных о сайте в список
    websites_data.append({website: html_code})

    # Случайная пауза
    time.sleep(random.randint(3, 5))

    # Сохранение данных о каждом сайте в отдельный JSON файл в папке json-s
    filename = f"json-s/{website}.json"
    with open(filename, 'w') as file:
        json.dump({website: html_code}, file)

    visited_count += 1

# Закрытие браузера
driver.quit()