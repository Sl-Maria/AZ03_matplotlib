# import requests
# from bs4 import BeautifulSoup
# import pprint
#
# url = "https://proxy.divan.ru/backend/category/get-products?slug=divany-i-kresla&page=1&isInit=true"
# response = requests.get(url)
# resp_json = response.json()
# pprint.pprint(resp_json)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

def create_data():
    url = "https://www.divan.ru/category/divany-i-kresla/"
    driver = webdriver.Chrome()
    parsed_data = []
    for i in range(1, 39):
        page_url = url + f"page-{i}"
        driver.get(page_url)
        divan_page = driver.find_elements(By.CLASS_NAME, 'wYUX2')
        for divan in divan_page:
            try:
                name = divan.find_element(By.TAG_NAME, 'span').text
                price = divan.find_element(By.TAG_NAME, 'meta').get_attribute('content')
                parsed_data.append([name, price])
            except:
                print("произошла ошибка при парсинге")
                continue
        time.sleep(3)
    driver.quit()

    if parsed_data:
        with open('divan.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Название', 'Цена'])
            writer.writerows(parsed_data)

def process_data():
    df = pd.read_csv('divan.csv', encoding='utf-8', index_col=0)
    # df.fillna(0, inplace=True)
    df['Цена'] = df['Цена'].astype(float)
    #print(df.describe())
    mean_price = df['Цена'].mean()
    print(f'Средняя цена диванов: {mean_price}')
    plt.hist(df['Цена'], bins=100)
    plt.show()


#create_data()
process_data()