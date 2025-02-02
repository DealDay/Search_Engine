# Title    : Connect to DB
# Filename : web_pages.py
# Author   : Adeola Ajala

# Imports
import random
import asyncio
import asyncio.coroutines

# fix module imports
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from search_engine import (WebPage, get_links_from_webpage, hash_function, 
                           binary_insert_url)
from fastapi import HTTPException
import motor.motor_asyncio


# connection to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://0.0.0.0:27017')#'mongodb://0.0.0.0:27017'
database = client.search_engine
collection = database.web_pages
visited_link = database.visited_web_pages

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
    # Allocate index for storage in DB
    index = hash_function(web_page)
    # Find if index exist in DB
    existing_urls = await collection.find_one({"index":index})
    if existing_urls:
        links = existing_urls['links']
        if web_page not in links:
            links.insert(binary_insert_url(links, web_page), web_page)
            response = await collection.update_one({'index':index},{'$set':{'links':links}})   
            if response:
                return "Link added successfully"
            raise HTTPException(404, "something went wrong")
    else:
        response = await collection.insert_one({"index":index, "links":[web_page]})
        if response:
            return "Link added successfully"
        raise HTTPException(404, "something went wrong") 

async def insert_visited_webpage(index:int, web_page:str, arr:list):
    """
    Insert one web page to visited web page DB
    index: insert location
    web_page: web page url
    arr: array to insert web_page
    """
    arr.insert(binary_insert_url(arr, web_page), web_page)
    response = await collection.update_one({'index':index},{'$set':{'links':arr}})
    if response:
        return "Successs" 
    raise HTTPException(404, "something went wrong")
    
async def insert_webpages_to_db(web_page_url:str):
    """
    Function to get all available links in a web page
    webPageURL: valid url
    """
    urls = await get_links_from_webpage(web_page_url)
    
    for url in urls:
        # Get href from url object
        link = url.get('href')
        # continue if not an external link
        if link == None or '.' not in link:
            continue
        # Add https to links without https
        if 'http' not in link:
            link = 'https:' + link
        # Allocate index for storage in DB
        index = hash_function(link)
        # Find if index exist in DB
        existing_index = await collection.find_one({"index":index})
        if existing_index:
            links = existing_index['links']
            if link not in links:
                links.insert(binary_insert_url(links, link), link)
                response = await collection.update_one({'index':index},{'$set':{'links':links}})   
                if response:
                    continue
                raise HTTPException(404, "something went wrong")
            else: continue    
        else:
            response = await collection.insert_one({"index":index, "links":[link]})
            if response:
                continue
            raise HTTPException(404, "something went wrong") 

async def web_page_crawler():
    # Generate a random number between 0 and 760 both included
    index = random.randint(0, 760)
    response = await collection.find_one({"index":index})

    if response:
        # Generate a random number between 0 and len(links)
        ind = random.randint(0, len(response['links']) - 1)
        url = response['links'][ind]
        # Check if link is already visited
        res = await visited_link.find_one({"index":index})
        if res:
            if url not in res['links']:
                # Get web_links from web page
                asyncio.run(insert_webpages_to_db(url))
                insert_visited_webpage(index, url, visited_link['links'])
        else:
            await insert_webpages_to_db(url)
            await visited_link.insert_one({"index":index, "links":[url]})

if __name__ == "__main__":
    # x = 0
    # # asyncio.set_event_loop(asyncio.new_event_loop())
    # while x < 10:
    #     asyncio.run(web_page_crawler())
    #     x += 1
    asyncio.run(web_page_crawler())
    # asyncio.run(insert_webpages_to_db('https://campus.w3schools.com/collections/certifications/products/xml-certificate'))
# End-of-file (EOF)
