from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
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
    #options.add_argument("--headless")
    driver = Chrome(
        service=ChromeService(executable_path=ChromeDriverManager().install()), options=options
    )
    
    return driver

async def clear_cookies(driver):
    driver.delete_all_cookies()
    
    
async def visit_website(driver, url):
    driver.get(url)  
     

async def refresh_page(driver):
    driver.refresh()
    

def values_exist(values, csv_file):
    df = pd.read_csv(csv_file)
    ref = df['Title'].values
    for data in ref:
        if str(data).lower() == values.lower():
            return True
        
    return False
    
    
    
async def next_button(driver):
     driver.execute_script("window.scrollBy(0, 100);")
     next = driver.find_element(By.CSS_SELECTOR,"#product-listing-container > div.pagination > ul > li.pagination-item.pagination-item--next > a")
     next.click()
     wait = WebDriverWait(driver, 25)
     wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    
async def click_product_details(driver):
    brand_page = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > div > div:nth-child(1) > div > div > div > a")
    await asyncio.sleep(1)
    #driver.execute_script("window.scrollBy(0, 700);")
    brand_page.click()
    


async def get_each_product_data(driver,link,img_link,url):
    dic_data = {}
    try:
      current_datetime = datetime.now()
      await asyncio.sleep(1)
      wait = WebDriverWait(driver, 25)
      wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
      Timespan = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
      title = driver.find_element(By.CLASS_NAME, "productView-title")
      SKU = driver.find_element(By.CLASS_NAME, "productView-info-value")
      sale_price = driver.find_element(By.XPATH, "/html/body/div[8]/div[1]/div/div[1]/section[1]/div/div[5]/div[2]/div[2]/span[3]")
      driver.execute_script("window.scrollBy(0, 200);")
      await asyncio.sleep(3)
      dic_data['Timespan'] = Timespan
      dic_data['Title']= title.text
      dic_data['SKU'] = SKU.text
      dic_data['Price']= sale_price.text
      dic_data['Image']= img_link
      dic_data['Url'] = url
      decription_ = driver.find_element(By.CLASS_NAME, "productView-description")
      table_data = decription_.find_elements(By.TAG_NAME, "li")
      list_data =[]
      for data in table_data:
          result_data = str(data.text).split(":")
          if result_data[0] !='' and len(result_data) > 1:
             list_data.append(' '.join(result_data[:]))
          else:
              list_data.append(result_data[0])
      dic_data["description"] =' '.join(list_data[:])
      return dic_data
    except Exception as err:
        print("error occur",err)
        return None
    
    
    
async def category(driver):
    wait = WebDriverWait(driver, 30)
    product_category = driver.find_element(By.CSS_SELECTOR, "#menu > nav > ul.navPages-list.marketplace")
    list_category = product_category.find_elements(By.CLASS_NAME, "navPages-item")
    url_list = []
    for item in list_category:
        try:
           link  = item.find_element(By.CLASS_NAME, "navPages-action")
           url = link.get_attribute("href")
           url_list.append(url)
           wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        except Exception as err:
            continue
    print(url_list)
    for url in url_list:
        try:
            print("hello")
            driver.get(url)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await get_all_data(driver)
        except Exception as err:
            continue
        
    
    
async def get_all_data(driver):
    driver.execute_script("window.scrollBy(0, 400);")
    csv_file = "shoestore.csv"
    wait = WebDriverWait(driver, 25)
    counter = 0
    unique_link = []
    while counter <= 100:
        list_products = driver.find_element(By.CLASS_NAME, "productGrid")
        data_results = list_products.find_elements(By.CLASS_NAME,"product--1")
        print(f"lenght of the data results is {len(data_results)}")
        try:
            for result in data_results:

                product_link = result.find_element(By.TAG_NAME, "a")
                link = product_link.get_attribute("href")
                product_img = result.find_element(By.TAG_NAME, "img").get_attribute("src")
                if link not in unique_link:
                   unique_link.append(link)
                   product_link.click()
                   data = await get_each_product_data(driver, product_link, product_img,link)   
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
                           if existing_header:
                               append_file = "a"
                           else:
                               append_file = 'w'   
                   else:
                        append_file = 'w'  
                   with open(csv_file, mode=append_file, newline='') as file:
                        writer = csv.writer(file)
                        if append_file == 'w':
                           writer.writerow(data.keys())
                        if not values_exist(str(data['Title']),csv_file):
                           writer.writerow(data.values())
                           pprint(data)
                        else:
                            print("value exist inside the csv...")
                   
                   driver.back()
                   wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                   await asyncio.sleep(3)
                   continue
                else:
                    continue
            driver.execute_script("window.scrollBy(0, 700);")
            try:
              await next_button(driver)
              
            except Exception as err:
                print("The next button not available on the page")
                return 
            await asyncio.sleep(3)
            counter += 1
        except (StaleElementReferenceException, NoSuchElementException, WebDriverException) as e:
            continue

        except Exception as err:
            #driver.back()
            current_url = driver.current_url
            if current_url == "https://shoestores.com/":
                await restart(driver)
                continue
            else:
                print(f"error occur: {err}")
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                await asyncio.sleep(3)
                continue
        

async def restart(driver):
    try:
          wait = WebDriverWait(driver, 25)
          wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
          await clear_cookies(driver)
          await asyncio.sleep(2)
          await click_product_details(driver)
          await asyncio.sleep(5)
          wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    except Exception as err:
         # print(err)
          await refresh_page(driver)
          wait = WebDriverWait(driver, 25)
          wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
   
               

async def main_(url):
    proxy_address = "socks5://194.163.134.97:1080"
    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"

    
    
    while True:
        driver = await setup_driver(proxy_address,user_agent)
        try:
            await visit_website(driver, url)
            # Wait until the page is fully loaded (timeout after 10 seconds)
            wait = WebDriverWait(driver, 25)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await clear_cookies(driver)
            await asyncio.sleep(2)
            await click_product_details(driver)
            #await asyncio.sleep(5)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await category(driver)
            print("why the code break")
            break
        
        except Exception as err:
            #print(err)
            await refresh_page(driver)
            wait = WebDriverWait(driver, 25)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        driver.quit()
        
    driver.quit()
    
    

        


