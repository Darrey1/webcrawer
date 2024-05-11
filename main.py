from crawler.app import main
from crawler.shoestore import main_
from crawler.soleprovision import main_func
from time import sleep
import asyncio

if __name__ =="__main__":
    while True:
        #(aperfectdealer website)
       #url = "https://www.aperfectdealer.com/"
       #asyncio.run(main(url))
       
       #(soleprovision website)
       url = "https://www.soleprovisions.com/"
       asyncio.run(main_func(url))
       
                                             #uncomment any website to run
       #(shoestore website)
       #url ="https://shoestores.com/"
       #asyncio.run(main_(url))
       
       sleep(3600)
    
    
 