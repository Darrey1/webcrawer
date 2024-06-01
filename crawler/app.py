from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import pandas as pd
import asyncio
from pprint import pprint
import json
import csv
import os
from datetime import datetime

async def setup_driver(address,user_agent):
    options = Options()
    options.add_argument("--disable-notifications")
    #options.add_argument(f"--proxy-server={address}")
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("--headless")
    driver = Chrome(
        service=ChromeService(executable_path=ChromeDriverManager().install()), options=options
    )
    
    return driver




async def visit_website(driver, url):
    driver.get(url)
    
    


async def clear_cookies(driver):
    driver.delete_all_cookies()
    
    
    
async def next_button(driver):
     ##pagination_next_bottom > a
     next = driver.find_element(By.CSS_SELECTOR,"#pagination_next_bottom > a")   
     next.click() 
     wait = WebDriverWait(driver, 10)
     wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    
    
async def refresh_page(driver):
    driver.refresh()
    
 
async def click_product_details(driver):
    link = driver.find_element(By.XPATH,'//*[@id="wid-key_1459408449128"]/div/div/div/h2/a')
    link.click()
    
    
    
def values_exist(values, csv_file):
    df = pd.read_csv(csv_file)
    ref = df['Refrence_number'].values
    for data in ref:
        if str(data).lower() == values.lower():
            return True
        
    return False
            


async def get_each_product_data(driver,link,url,image_link):
    current_datetime = datetime.now()

    Timespan = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    dic_data = {}
    await asyncio.sleep(1)
    link.click()
    wait = WebDriverWait(driver, 30)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    title = driver.find_element(By.CSS_SELECTOR,"#content > div > div.primary_block > div > div.pb-right-column.col-xs-12.col-sm-12.col-md-6.col-lg-6 > h1")
    refrence_number = driver.find_element(By.CSS_SELECTOR,"#product_reference > span")
    description = driver.find_element(By.CSS_SELECTOR, "#short_description_content")
    price = driver.find_element(By.ID, "our_price_display")
    await asyncio.sleep(3)
    dic_data['Date'] = Timespan
    dic_data['Title']= title.text
    dic_data['Refrence_number']= refrence_number.text
    dic_data['Description']= description.text
    dic_data['Price']= price.text
    dic_data['Image'] = image_link
    dic_data['Url'] = url
    driver.execute_script("window.scrollBy(0, 700);")
    try:
       product_details = driver.find_element(By.CSS_SELECTOR, "#content > div > div.pts-tab.pts-tab-product.tab-v4 > ul > li:nth-child(2) > a")
       await asyncio.sleep(1)
       product_details.click()
       driver.execute_script("window.scrollBy(0, 400);")
    except Exception as arr:
        return None 
    await asyncio.sleep(3)
    product_datasheet = driver.find_element(By.CLASS_NAME, "table-data-sheet")
    table_data = product_datasheet.find_elements(By.TAG_NAME, "tr")
    for data in table_data:
        result_data = str(data.text).split(" ")
        if result_data and len(result_data) > 1:
           dic_data[result_data[0]] = ' '.join(result_data[1:])
        else:
            dic_data["Description"] += " " + result_data[:]

    return dic_data




async def category(driver):
       wait = WebDriverWait(driver, 30)
       wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
       category_url = driver.find_element(By.ID, "right_column")
       category_list = category_url.find_elements(By.TAG_NAME, 'li')
       url_list = []
       for category in category_list:
           try:
              url = category.find_element(By.TAG_NAME, "a").get_attribute('href')
              url_list.append(url)
              wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
           except Exception as err:
              continue
       for url in url_list:
        try:
            print("hello")
            driver.get(url)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await get_all_data(driver)
        except Exception as err:
            continue
        
        
    
async def get_all_data(driver):
    csv_file = "output.csv"
    wait = WebDriverWait(driver, 30)
    counter = 0
    unique_link = []
    while counter <= 100:
        
        data_results = driver.find_elements(By.CLASS_NAME,"owl-wrapper")
        print(f"lenght of the data results is {len(data_results)}")
        try:   
            for index,result in enumerate(data_results):
                img_url = result.find_element(By.TAG_NAME, 'img')
                image_link = img_url.get_attribute('src')
                product_link = result.find_element(By.CLASS_NAME,'product-name')
                link = product_link.get_attribute("href")
                if link not in unique_link:
                   unique_link.append(link)
                   url = product_link.get_attribute("href")
                   product_link.click()
                   driver.back()
                   data = await get_each_product_data(driver, product_link, url,image_link)
           
                   if data is None:
                       driver.back()
                       print("the return data is none")
                       wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                       continue
                 
                 
                   if os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0:
                       with open(csv_file, mode='r') as file:
                           reader = csv.reader(file)
                           existing_header = next(reader, None)
                           #if existing_header == list(data.keys()):
                           if existing_header and len(existing_header) > 13:
                               append_file = "a"
                           else:
                               append_file = 'w'
                           
                   else:
                        append_file = 'w'
                      
                      
                    
                   with open(csv_file, mode=append_file, newline='') as file:
                        writer = csv.writer(file)
                        if append_file == 'w':
                           writer.writerow(data.keys())
                        if len(data.values()) <= 24:
                           if not values_exist(str(data['Refrence_number']),csv_file):
                              writer.writerow(data.values())   
                              pprint(data) 
                           else:
                               print("skipping... value exist inside the csv")
                        else:
                            print("skipping ....value not valid")
                           
                   
                                
                   
                   driver.back()
                   wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                   await asyncio.sleep(3)
                   continue
            try:
               await next_button(driver)
               await asyncio.sleep(3) 
            except Exception as err:
                print("The next button not available on the page")
                return
            counter += 1
        except Exception as err:
            driver.back()
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await asyncio.sleep(3)
            continue
        
        
        
    
async def main(url):
    proxy_address = "socks5://194.163.134.97:1080"
    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"

    
    
    while True:
        driver = await setup_driver(proxy_address,user_agent)
        try:
            await visit_website(driver, url)
            wait = WebDriverWait(driver, 30)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await clear_cookies(driver)
            await asyncio.sleep(2)
            await click_product_details(driver)
            await asyncio.sleep(5)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await category(driver)
            break
        
        except Exception as err:
            print(err)
            await refresh_page(driver)
            wait = WebDriverWait(driver, 30)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        driver.quit()
        
    driver.quit()
        
        
