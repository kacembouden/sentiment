# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 13:29:33 2023

@author: kacem
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from datetime import datetime, timedelta

import time


def create_url(item,date_start,date_end):
    url = 'https://www.google.com/search?q=' + item + '&tbm=nws&tbs=cdr:1,cd_min:' + date_end + ',cd_max:' + date_end + '&gl=us&num=500'
    return url
    

def get_page_data(url):
    driver.get(url)
    content = driver.find_elements(By.CLASS_NAME, "iRPxbe")
    datas = []
    for article in content :
        article.text
        lines = article.text.split("\n")
        data = {"source" : lines[0] , "title" : lines[1] ,"discreption" : lines[2] ,"date" : lines[4] ,}
        datas.append(data)
        df = pd.DataFrame(datas)
        return df
        
    #print("--- %s seconds ---" % (time.time() - start_time))

def save_file(df, date):
    
    file_name = item+ '-' + date.replace("/" , '-') 
    df.to_csv("C:/Users/kacem/OneDrive/Bureau/D/data/" + file_name, sep=',')
    


start_date = datetime(2022,11, 13)
end_date = datetime(2023, 7, 27)

date_range = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]

driver = webdriver.Chrome('chromedriver')

item = 'bitcoin'


for date in date_range:
    day = date.day
    month = date.month
    year = date.year
    date_start = str(month) + '/' + str(day) + '/' + str(year)
    date_end = str(month) + '/' + str(day + 1) + '/' + str(year)
    url = create_url(item,date_start,date_end)
    driver.get(url)
    
    if 'google.com/sorry' in driver.current_url :
        driver.close()
        time.sleep(5)
        driver = webdriver.Chrome('chromedriver')
        driver.get(url)
    
    
    content = driver.find_elements(By.CLASS_NAME, "iRPxbe")
    datas = []
    for article in content :
        article.text
        lines = article.text.split("\n")
        data = {"source" : lines[0] , "title" : lines[1] ,"discreption" : lines[2] ,"date" : lines[4] ,}
        datas.append(data)
        df = pd.DataFrame(datas)
    
    
    print(df)
    
    save_file(df, date_start)
    time.sleep(20)
    
    
    





