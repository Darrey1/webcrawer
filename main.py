from crawler.app import main
#from crawler.app2 import main_func
from time import sleep
import asyncio

if __name__ =="__main__":
    while True:
       url = "https://www.aperfectdealer.com/"
       #asyncio.run(main(url))
       #url = "https://shoestores.com/"
       asyncio.run(main(url))
       sleep(3600)
    
    
