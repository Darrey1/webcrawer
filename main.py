from crawler.app import main
from crawler.shoestore import main_
from crawler.soleprovision import main_func
from time import sleep
import asyncio
import threading
from web.page import streamlit_app

async def scrape_data():
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
     

async def main_loop():
    while True:
        await scrape_data()
        await asyncio.sleep(3600) 

def start_async_tasks():
    asyncio.run(main_loop())

if __name__ == "__main__":
    # Start the async tasks in a separate thread
    threading.Thread(target=start_async_tasks).start()

    # Run Streamlit in the main thread
    streamlit_app()
    
 
