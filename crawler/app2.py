from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import asyncio
from pprint import pprint
import json
import csv
import os


async def setup_driver(address,user_agent):
    options = Options()
    options.add_argument("--disable-notifications")
    #options.add_argument(f"--proxy-server={address}")
    options.add_argument(f'--user-agent={user_agent}')
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
    
    
async def click_product_details(driver):
    brand_page = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(7) > div > div:nth-child(1) > div > div > div > a")
    await asyncio.sleep(1)
    driver.execute_script("window.scrollBy(0, 700);")
    brand_page.click()
    


async def get_each_product_data(driver,link):
    dic_data = {}
    await asyncio.sleep(1)
    link.click()
    wait = WebDriverWait(driver, 20)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    await asyncio.sleep(2)
    try:
       product_description = driver.find_element(By.CLASS_NAME, "productView-title")
       print("the title is scrapped")
    except Exception as err:
        print(err)
        return
    print(product_description.text)
    

    
    
async def get_all_brand_data(driver):
       main_prduct_page = driver.find_element(By.CLASS_NAME, "productGrid")
       product_data = main_prduct_page.find_elements(By.TAG_NAME, "li")
       wait = WebDriverWait(driver, 15)
       #print(f"brand number is {len(product_data)}")
       while True:
        try:
          for data_value in product_data:
              product_link = data_value.find_element(By.CLASS_NAME,"card-figure")
              link_tag = product_link.find_element(By.TAG_NAME,"a")
              link = product_link.find_element(By.TAG_NAME,"a").get_attribute("href")
              print(link)
              await asyncio.sleep(2)
              await get_each_product_data(driver, link_tag)
              driver.back()
              wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
              continue
              
          return
                    
        except Exception as err:
             print(f"perhaps an error occur!: {err}")
             wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
             continue
   
               

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
            #await asyncio.sleep(5)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            await get_all_brand_data(driver)
            print("why the code break")
            break
        
        except Exception as err:
            print(err)
            await refresh_page(driver)
            wait = WebDriverWait(driver, 10)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        driver.quit()
        
    driver.quit()
        


