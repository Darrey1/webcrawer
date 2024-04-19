from crawler.app import main
from time import sleep
import asyncio

if __name__ =="__main__":
    while True:
       url = "https://www.aperfectdealer.com/"
       asyncio.run(main(url))
       sleep(3600)
    
    
