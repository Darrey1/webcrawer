from crawler.app import main
from crawler.shoestore import main_
from crawler.soleprovision import main_func
from time import sleep
import asyncio
import threading

async def func():
      #(aperfectdealer website)
     # url1 = "https://www.aperfectdealer.com/"
     #(soleprovision website)
     #url2 = "https://www.soleprovisions.com/"
     
     #(shoestore website)
     url3 ="https://shoestores.com/"
     print("Starting running...")
     print("make sure your have strong internet connection...")
     #await asyncio.gather(main(url1),main_(url3))
     await asyncio.run(main(url3))
     


if __name__ =="__main__":
    while True:
         asyncio.run(func())
                                            
         sleep(3600)
    
    
 
