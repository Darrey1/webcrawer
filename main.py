from crawler.app import main
from crawler.shoestore import main_
from crawler.soleprovision import main_func
from time import sleep
import asyncio
import threading

async def func():
      #(aperfectdealer website)
     url1 = "https://www.aperfectdealer.com/"
     ##(soleprovision website)
     url2 = "https://www.soleprovisions.com/"
     
     #(shoestore website)
     url3 ="https://shoestores.com/"
     threads = []
     runner = await asyncio.gather(main(url1), main_func(url2), main_(url3))
     print("Starting running...")


if __name__ =="__main__":
    while True:
        asyncio.run(func())
        sleep(3600)
    
    
 