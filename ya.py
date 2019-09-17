from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys

import re

lst = [
'ОАО "Ставропольская ГРЭС"',
'ОАО "Волжская ГЭС"',
'Каскад ВВ ГЭС',
'ОАО "Зейская ГЭС"',
'АО "ЧЭМК"',
'Красноярскэнерго',
'ОАО ""Ярэнерго"',
'ПАО ""Ульяновскэнерго"',
'ОАО ""Оренбургэнерго"',
'АО ""Каббалкэнерго"'
]

driver = webdriver.Chrome()

driver.get('https://yandex.ru')

for it in lst:
    elem = driver.find_element_by_xpath("//input[contains(@class, 'input__control')]")
    print(elem.text)
    elem.clear()
    elem.send_keys(f'{it} официальный сайт')

    elem.send_keys(Keys.RETURN)

    elem1 = driver.find_element_by_xpath("//a[@class='link link_theme_outer path__item i-bem']")
    print(elem1.text)
    print(re.findall(r'\s*(\w+\.\w{2,3})', elem1.text))