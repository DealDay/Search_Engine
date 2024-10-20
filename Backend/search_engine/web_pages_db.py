# Title    : Connect to DB
# Filename : web_pages.py
# Author   : Adeola Ajala

# Imports
import asyncio.coroutines
from fastapi import HTTPException
from search_engine import WebPage
import motor.motor_asyncio
import requests
from bs4 import BeautifulSoup
import asyncio

# connection to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://0.0.0.0:27017')#'mongodb://0.0.0.0:27017'
database = client.search_engine
collection = database.web_pages

async def fetch_all_webPages():
    webPages = []
    cursor = collection.find({})
    async for document in cursor:
        webPages.append(WebPage(**document))
    return webPages

async def insert_one_webPage(webPage):
    """
    Insert one web page to DB
    webPage: web page url
    """
    await collection.insert_one(webPage)
    return webPage

async def get_links_from_webpage(webPageURL:str):
    """
    Function to get all available links in a web page
    webPageURL: valid url
    """
    req = requests.get(webPageURL)
    soup = BeautifulSoup(req.text, 'html.parser')
    urls = soup.find_all('a')
    links = []
    for url in urls:
        link = url.get('href')
        if 'https' not in link:
            link = 'https:' + link
        links.append(link)
    response = await collection.insert_many([{"url": link} for link in links])
    if response:
        return
    raise HTTPException(404, "something went wrong")
    
if __name__ == "__main__":
    asyncio.run(get_links_from_webpage('https://www.wikipedia.org'))
# End-of-file (EOF)
