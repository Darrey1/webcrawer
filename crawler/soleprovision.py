from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import threading
import time
import asyncio
from pprint import pprint
import json
import csv
import os
from time import sleep

async def setup_driver(address,user_agent):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument(f"--no-sandbox")
    options.add_argument(f'--user-agent={user_agent}')
    driver = Chrome(
        service=ChromeService(executable_path=ChromeDriverManager().install()), options=options
    )

    return driver

async def visit_website(driver, url):
    driver.get(url)

async def clear_cookies(driver):
    driver.delete_all_cookies()
    

async def next_button(driver):
    #//*[@id="gf-products"]
     driver.execute_script("window.scrollBy(0, 600);")
     next = driver.find_element(By.CLASS_NAME,"next")
     next.click()
     wait = WebDriverWait(driver, 10)
     wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")


async def refresh_page(driver):
    driver.refresh()


async def click_product_details(driver):
    driver.execute_script("window.scrollBy(0, 300);")
    link = driver.find_element(By.XPATH,'//*[@id="Banner-desktop_banner"]')
    link.click()



def values_exist(values, csv_file):
    if not os.path.isfile(csv_file):
        return False
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if all(value in row for value in values):
                return True

    return False

async def get_each_product_data(driver,link,img_link):
    dic_data = {}
    try:
      
      await asyncio.sleep(1)
      wait = WebDriverWait(driver, 10)
      wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
      title = driver.find_element(By.CLASS_NAME, "product__title")
      sale_price = driver.find_element(By.CLASS_NAME, "price-item")
      driver.execute_script("window.scrollBy(0, 200);")
      await asyncio.sleep(3)
      dic_data['Title']= title.text
      dic_data['sale_price']= sale_price.text
      dic_data['image']= img_link
      return dic_data
    except Exception as err:
        print("error occur",err)
        return None
    



async def get_all_data(driver):
    csv_file = "soleprovision.csv"
    wait = WebDriverWait(driver, 25)
    counter = 0
    unique_link = []
    while counter <= 100:
        #product = driver.find_element(By.XPATH, '//*[@id="gf-products"]')
        data_results = driver.find_elements(By.CLASS_NAME,"spf-col-xl-4")
        print(f"lenght of the data results is {len(data_results)}")
        try:
            for result in data_results:

                product_link = result.find_element(By.TAG_NAME, "a")
                link = product_link.get_attribute("href")
                product_img = result.find_element(By.TAG_NAME, "img").get_attribute("src")
                print(product_img)
                if link not in unique_link:
                   unique_link.append(link)
                   pprint(product_link.get_attribute("href"))
                   product_link.click()
                   #driver.back()
                   data = await get_each_product_data(driver, product_link, product_img)   
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
                        print("check if this place will be printed")
                        if append_file == 'w':
                           writer.writerow(data.keys())
                        if not values_exist(data.values(),csv_file):
                           writer.writerow(data.values())
                        print("this may be printed")
                   pprint(data)
                   driver.back()
                   wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                   await asyncio.sleep(3)
                   continue
                else:
                    continue
            await next_button(driver)
            await asyncio.sleep(3)
            counter += 1
        except Exception as err:
            #driver.back()
            current_url = driver.current_url
            if current_url == "https://www.soleprovisions.com/":
                await restart(driver)
                continue
            else:
                print(f"error occur: {err}")
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                await asyncio.sleep(3)
                continue
        

async def restart(driver):
    try:
          wait = WebDriverWait(driver, 20)
          wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
          await clear_cookies(driver)
          await asyncio.sleep(2)
          await click_product_details(driver)
          await asyncio.sleep(5)
          wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    except Exception as err:
          print(err)
          await refresh_page(driver)
          wait = WebDriverWait(driver, 10)
          wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

async def main_func(url):
    proxy_address = "socks5://194.163.134.97:1080"
    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"



    while True:
        driver = await setup_driver(proxy_address,user_agent)
        
        try:
            await visit_website(driver, url)
            # Wait until the page is fully loaded (timeout after 10 seconds)
            wait = WebDriverWait(driver, 10)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await clear_cookies(driver)
            await asyncio.sleep(2)
            await click_product_details(driver)
            await asyncio.sleep(5)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await get_all_data(driver)
            break

        except Exception as err:
            print(err)
            await refresh_page(driver)
            wait = WebDriverWait(driver, 10)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        driver.quit()

    driver.quit()
    

