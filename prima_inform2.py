from selenium import webdriver          #Основной элемент
from selenium.webdriver.common.keys import Keys    #Клавиши клавиатуры
import re
from pymongo import MongoClient

import time

import csv
data = [
    ['INN', 'inn_check', 'Name', 'ni']
]
print(time.ctime())

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
    reader = csv.DictReader(file_obj, delimiter=';')
    for line in reader:
        inn = line["INN"]
        name = line["Name"]
        print(name + ' ' + inn)

        elem = driver.find_element_by_id("query")
        elem.clear()
        elem.send_keys(name)

        elem.send_keys(Keys.RETURN)
        #  time.sleep(3)

        ni = ''
        incheck = ''

        try:
            elem_ni = driver.find_element_by_xpath('//strong[text()="Код налогового органа:"]/..')
            print(elem_ni.text)
            div_ni = re.findall(r'Код налогового органа:\s*(\d+)\s*\(', elem_ni.text)
            print('*****', div_ni)

            elem_inncheck = driver.find_element_by_xpath('//strong[text()="ИНН:"]/..')
            print('elem_inncheck', elem_inncheck.text)
            inncheck = re.findall(r'ИНН:\s*(\d+)', elem_inncheck.text)[0]

            if div_ni:
                ni = div_ni[0].strip()
                print('-----------------------', ni)
        except:
            print(f'{name} - error')
            elem = driver.find_element_by_id("query")
            elem.clear()
            elem.send_keys(inn)
            elem.send_keys(Keys.RETURN)
            #  time.sleep(3)
            try:
                elem_ni = driver.find_element_by_xpath('//strong[text()="Код налогового органа:"]/..')
                print(elem_ni.text)
                div_ni = re.findall(r'Код налогового органа:\s*(\d+)\s*\(', elem_ni.text)
                print('*****', div_ni)

                elem_inncheck = driver.find_element_by_xpath('//strong[text()="ИНН:"]/..')
                print('elem_inncheck', elem_inncheck.text)
                inncheck = re.findall(r'ИНН:\s*(\d+)', elem_inncheck.text)[0]

                if div_ni:
                    ni = div_ni[0].strip()
                    print('-----------------------', ni)
            except:
                print(f'{name + inn} - error')

        print('----------------------------------------')
        data.append([inn, inncheck, name, ni])
        csv_writer(data, "output_ni.csv")


driver = webdriver.Chrome()

driver.get('https://www.prima-inform.ru')

with open("ca1.csv") as f_obj:
        csv_dict_reader(f_obj)

driver.close()
print(time.ctime())

# client = MongoClient('mongodb://127.0.0.1:27017')
#
# db = client['prima_db']
# nalog_insp = db.nalog
# nalog_insp.drop()


# assert "GeekBrains" in driver.title

#Заполняем поле для ввода
  # логин

# elem = driver.find_element_by_id("mailbox:password")
# elem.send_keys('tobeornot1')  # пароль

# for i in range(len(elems)):
#
#     it = elems[i]
#
#     x_from = it.find_element_by_xpath('.//span[contains(@class,"ll-crpt")]').text
#     x_subj = it.find_element_by_xpath('.//span[contains(@class,"llc__subject")]').text
#     x_time = it.find_element_by_xpath('.//div[@class="llc__item llc__item_date"]').text
#
#     it.click()
#
#     time.sleep(4)
#     body_elem = driver.find_element_by_xpath('//div[@class="letter__body"]')
#     x_body = body_elem.text
#
#     letter_data = {
#         'from': x_from,
#         'subj': x_subj,
#         'date_time': x_time,
#         'body': x_body
#     }
#
#     lesson6.insert_one(letter_data)
#
#     driver.back()
#     time.sleep(4)
#     elems = driver.find_elements_by_xpath('//div[@class="llc__content"]')



