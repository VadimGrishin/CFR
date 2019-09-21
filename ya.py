from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys

import re

import time

import csv

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """

    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)
def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """

    global data

    reader = csv.DictReader(file_obj, delimiter=';')
    for line in reader:

        inn = line["INN"]
        name = line["Name"]
        print('from csv: ', name + ' ' + inn)

        elem = driver.find_element_by_xpath("//input[contains(@class, 'input__control')]")
        print('----------------------')
        elem.clear()
        elem.send_keys(f'{name} официальный сайт')

        elem.send_keys(Keys.RETURN)

        elems = driver.find_elements_by_xpath("//a[@class='link link_theme_outer path__item i-bem']")

        x0, x1 = '', ''
        for i, it in enumerate(elems):
            if i == 0:
                x0 = it.text
            elif i == 1:
                x1 = it.text
            else:
                break

        data.append([inn, name, x0, x1])
        csv_writer(data, "output_ya_site.csv")

data = [
    ['INN', 'Name', 'site1', 'site2']
]

driver = webdriver.Chrome()

driver.get('https://yandex.ru')

with open("input.csv") as f_obj:
    csv_dict_reader(f_obj)

# lst = [
# 'ОАО "Ставропольская ГРЭС"',
# 'ОАО "Волжская ГЭС"',
# 'Каскад ВВ ГЭС',
# ]

# 'ОАО "Зейская ГЭС"',
# 'АО "ЧЭМК"',
# 'Красноярскэнерго',
# 'ОАО ""Ярэнерго"',
# 'ПАО ""Ульяновскэнерго"',
# 'ОАО ""Оренбургэнерго"',
# 'АО ""Каббалкэнерго"'

# for it in lst:
#     elem = driver.find_element_by_xpath("//input[contains(@class, 'input__control')]")
#     print('----------------------')
#     elem.clear()
#     elem.send_keys(f'{it} официальный сайт')
#
#     elem.send_keys(Keys.RETURN)
#
#     elems = driver.find_elements_by_xpath("//a[@class='link link_theme_outer path__item i-bem']")
#     for i, it in enumerate(elems):
#         if i > 1:
#             break
#         print(it.text)
#         print(re.findall(r'\s*(\w+\.\w*\.?\w{2,3})', it.text))
#     else:
#         print('not found')