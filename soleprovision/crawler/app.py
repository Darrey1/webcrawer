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

     driver.execute_script("window.scrollBy(0, 600);")
     next = driver.find_element(By.CLASS_NAME,"next")
     next.click()
     wait = WebDriverWait(driver, 10)
     wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")


async def refresh_page(driver):
    driver.refresh()


async def click_product_details(driver):
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

async def get_each_product_data(driver,link):
    dic_data = {}
    await asyncio.sleep(1)
    link.click()
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    title = driver.find_element(By.CSS_SELECTOR, "#ProductInfo-template--16852200849646__main > div.product__title > h2")
    price = driver.find_element(By.CSS_SELECTOR, "#price-template--16852200849646__main > div > div > div.price__regular > span.bold_option_price_display.price-item.price-item--regular")
    color = driver.find_element(By.CSS_SELECTOR, "#swatch-option1 > div > fieldset > legend > label > span.swatch-variant-name")
    swatch_image = driver.find_element(By.CSS_SELECTOR, "#swatch-option1 > div > fieldset > ul > li > div.swatch-image.swatch-selector.swatch-selected.swatch-allow-animation > div.star-set-image")
    size = driver.find_element(By.CSS_SELECTOR, "#swatch-option2 > div > fieldset > ul > li:nth-child(2) > div > div.swatch-button-title-text")
    width = driver.find_element(By.CSS_SELECTOR, "#swatch-option3 > div > fieldset > ul > li > div > div.swatch-button-title-text > span")
    try:
        # Try finding clickable description element (approach 1)
        description = driver.find_element(By.CSS_SELECTOR, "#ProductInfo-template--16852200849646__main > div:nth-child(9) > div > div:nth-child(1) > div > p")
    except NoSuchElementException:
        # Description might be in a dropdown, find the trigger element and click
        description_trigger = driver.find_element(By.CSS_SELECTOR, "#ProductInfo-template--16852200849646__main > div:nth-child(9) > div > div:nth-child(1) > label")
        description_trigger.click()
        await asyncio.sleep(1)  # Wait for description to load
        description = driver.find_element(By.CSS_SELECTOR, "#short_description_content")  # Find description again

    image = driver.find_element(By.TAG_NAME, "img")
    image_link = image.get_attribute('src')
    await asyncio.sleep(3)
    dic_data['Title']= title.text
    dic_data['Price']= price.text
    dic_data['Color']= color.text
    dic_data['SwatchImage']= swatch_image.text
    dic_data['Size']= size.text
    dic_data['Width']= width.text
    dic_data['Description']= description.text
    driver.execute_script("window.scrollBy(0, 700);")
    html_content = driver.page_source  # Get the current page source (HTML content)
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.select('.product-media-modal__content img')  # Adjust selector if needed

    image_links = []
    for image in images:
        image_link = image.get_attribute('src')
        image_links.append(image_link)

    dic_data['Image Links'] = image_links
    return dic_data



async def get_all_data(driver):
    csv_file = "soleprovision.csv"
    wait = WebDriverWait(driver, 15)
    counter = 0
    unique_link = []
    while counter <= 100:
        
        data_results = driver.find_elements(By.CLASS_NAME,"spf-col-xl-4")
        print(f"lenght of the data results is {len(data_results)}")
        try:
            for index,result in enumerate(data_results):

                product_link = result.find_element(By.CSS_SELECTOR, value="div[class='spf-product__info'] div a")
                link = product_link.get_attribute("href")
                if link not in unique_link:
                   unique_link.append(link)
                   pprint(product_link.get_attribute("href"))
                   product_link.click()
                   driver.back()
                   data = await get_each_product_data(driver, product_link)

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
            await next_button(driver)
            await asyncio.sleep(3)
            counter += 1
        except Exception as err:
            driver.back()
            print(f"error occur: {err}")
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
