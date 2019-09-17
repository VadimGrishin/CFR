from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys    #Клавиши клавиатуры
import re
from pymongo import MongoClient

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

    global data, resp1s

    reader = csv.DictReader(file_obj, delimiter=';')
    for line in reader:

        inn = line["INN"]
        name = line["Name"]
        print('from csv: ', name + ' ' + inn)

        select_name(inn, name)


def select_name(inn, name):
    global data, resp1s
    time.sleep(5)
    driver.get('https://www.list-org.com/')

    resp1s.append(driver.page_source)

    if 'вы не робот' in driver.page_source:
        print('---- в жбан True')
        exit()

    elem = driver.find_element_by_xpath("//input[@placeholder='Поиск']")
    elem.clear()
    elem.send_keys(inn)

    elem.send_keys(Keys.RETURN)

    blocks = driver.find_elements_by_xpath('//div[@class="org_list"]/p')  # все организации по данному inn

    companies = []
    for block in blocks:  # выбираем корректные компании для последующего перебора

        try:
            x = block.find_element_by_xpath('.//label/a')
        except:
            x = ''

        if x:
            check_name = x.text
            cmnt = block.find_element_by_xpath('.//label/span').text
            href = block.find_element_by_xpath('.//label/a').get_attribute('href')

            name_idx = name.upper().replace('ОАО ', '').replace('ЗАО ', '').replace('ПАО ', '').replace('АО ', '').\
                replace('ООО ', '').replace(' ', '').replace('"', '').replace('-', '').replace(',', '').replace('.', '')\
                .replace('«', '').replace('»', '')
            check_name_idx = check_name.upper().replace('ОАО ', '').replace('ЗАО ', '').replace('ПАО ', '').replace('АО ', '').\
                replace('ООО ', '').replace(' ', '').replace('"', '').replace('-', '').replace(',', '').replace('.', '')\
                .replace('«', '').replace('»', '')


            print(name_idx, check_name_idx)
            if name_idx == check_name_idx:

                companies.append([check_name, cmnt, href])

    print('отобрано компаний: ', companies)

    for company in companies:
        e_mail = ''
        site = ''
        driver.get(company[2])  # страница компании

        resp1s.append(driver.page_source)

        if 'вы не робот' in driver.page_source:
            print('---- в жбан True')
            exit()
        print('---- в жбан False')

        try:
            e_mail = driver.find_element_by_xpath(
                '//i[@class="fa-sm fa fa-at fa-fw"]/../..//a').text
        except:
            pass
        print('----------------', e_mail)

        try:
            site = driver.find_element_by_xpath('//div[@class="sites"]/p/a').text
        except:
            pass
        print('----------------', site)

        try:
            x = driver.find_element_by_xpath('//div[@class="header"]/h1').text
            print('----------------', x)
            check_name2 = x.replace('Организация ', '').strip()
        except:
            check_name2 = ''

        data.append([inn, name, company[0], company[1], company[2], check_name2, e_mail, site])
        csv_writer(data, "output_email_site.csv")


data = [
    ['INN', 'Name', 'inn_check', 'cmnt', 'href', 'check_name2', 'e_mail', 'site']
]

resp1s =[]
print(time.ctime())

driver = webdriver.Chrome()

with open("input_ost.csv") as f_obj:
        csv_dict_reader(f_obj)

driver.close()
print(time.ctime())
