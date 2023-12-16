# import relevant packages
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSessionIdException
import time
from time import sleep
import copy
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# open selenium driver
main_url='https://finance.yahoo.com/most-active/?offset=0&count=250'
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.get(main_url)

# obtain list of 250 most active stock tickers
ticker_symbol_list=[]
for i in range(1, 251):
    element=driver.find_element(By.XPATH,'//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[1]/a')
    ticker_symbol_list.append(element.text)
    
ticker_urls=[]
for ticker in ticker_symbol_list:
    url='https://finance.yahoo.com/quote/'+ticker+'/history?p='+ticker
    ticker_urls.append(url)
    
i=0 # keep track of current status

# loop through ticker_urls and download historical data to folder
for url in ticker_urls[i:]:
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : '/Users/joyceee_xby/Desktop/Project/stock_data'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
    except TimeoutException as Exception:
        driver.close()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        continue
    sleep(10)
    button = driver.find_element(By.XPATH,'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div')
    try:
        button.click()
    except NoSuchElementException as Exception:
        driver.close()
        driver.get(url)
        sleep(10)
        button.click()
        continue
    sleep(3)
    button2 = driver.find_element(By.XPATH,'//*[@id="dropdown-menu"]/div/ul[2]/li[3]')
    button2.click()
    sleep(5)
    link=driver.find_element(By.XPATH,'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
    download_link = link.get_attribute('href')
    r=driver.get(download_link)
    sleep(3)
    driver.quit()
    print("Successfully downloaded:", ticker_symbol_list[i])
    i+=1