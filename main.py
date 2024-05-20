from crawler.app import main
from crawler.shoestore import main_
from crawler.soleprovision import main_func
from time import sleep
import asyncio
import threading
from web.page import streamlit_app

async def func():
      #(aperfectdealer website)
     url1 = "https://www.aperfectdealer.com/"
     #(soleprovision website)
     #url2 = "https://www.soleprovisions.com/"
     
     #(shoestore website)
     url3 ="https://shoestores.com/"
     print("Starting running...")
     print("make sure your have strong internet connection...")
     await asyncio.gather(main(url1),main_(url3))
     

async def main_loop():
    while True:
        await func()
        await asyncio.sleep(3600)  # Wait for 1 hour

def start_streamlit():
    streamlit_app()

if __name__ == "__main__":
    # Start the Streamlit app in a separate thread
    threading.Thread(target=start_streamlit, daemon=True).start()

    # Run the main_loop in the asyncio event loop
    asyncio.run(main_loop())

