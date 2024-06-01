from crawler.shoestore import main_
from time import sleep
import asyncio

if __name__ =="__main__":
    while True:
       url = "https://shoestores.com/"
       asyncio.run(main_(url))
       sleep(3600)
