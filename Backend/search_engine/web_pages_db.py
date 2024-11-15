# Title    : Connect to DB
# Filename : web_pages.py
# Author   : Adeola Ajala

# Imports
import asyncio
import asyncio.coroutines
import requests
from bs4 import BeautifulSoup
# fix module imports
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from search_engine import WebPage, get_links_from_webpage, hash_function
from fastapi import HTTPException
import motor.motor_asyncio


# connection to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://0.0.0.0:27017')#'mongodb://0.0.0.0:27017'
database = client.search_engine
collection = database.web_pages

async def fetch_all_webpages():
    """
        get all web pages from DB
    """
    webpages = []
    cursor = collection.find({})
    async for document in cursor:
        webpages.append(WebPage(**document))
    return webpages

async def insert_one_webpage(web_page):
    """
    Insert one web page to DB
    webPage: web page url
    """
    await collection.insert_one(web_page)
    return web_page

async def insert_webpages_to_db(web_page_url:str):
    """
    Function to get all available links in a web page
    webPageURL: valid url
    """
    urls = get_links_from_webpage(web_page_url)
    for url in urls:
        link = url.get('href')
        hash_value, index = hash_function(url)
        existing_urls = await collection.find_one({"index":index})
        if existing_urls:
            links = existing_urls.links
        else:
            if 'http' not in link:
                link = 'https:' + link
            response = await collection.insert_one({"index":index, "links":[link]})
        
    if response:
        return
    raise HTTPException(404, "something went wrong")
if __name__ == "__main__":
    asyncio.run(get_links_from_webpage('https://www.wikipedia.org'))
# End-of-file (EOF)
