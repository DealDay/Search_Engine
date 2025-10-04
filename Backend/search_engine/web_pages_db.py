# Title    : Connect to DB
# Filename : web_pages.py
# Author   : Adeola Ajala

# Imports
import random
import asyncio
import asyncio.coroutines
from rank_bm25 import BM25Okapi
# from .model import *
# from .search_engine_functions import * 

# fix module imports
import sys
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from search_engine import *
from fastapi import HTTPException
import motor.motor_asyncio


# connection to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://0.0.0.0:27017')#'mongodb://0.0.0.0:27017'
database = client.search_engine
collection = database.web_pages
crawled_link = database.crawled_web_pages
reverse_index = database.page_index

async def search_query_in_db(query:list):
    """
    return web pages that conatain search query
    query: list of search query
    return web pages with search query
    """
    # print(query)
    search_info = []
    for queries in query:
        data = await reverse_index.find_one({"index":queries})
        for x in range(len(data['pages'])):
            # print(data['pages'][x]['url'])
            if data['pages'][x] not in search_info:
                # print('yes')
                search_info.append(data['pages'][x])
    return search_info

async def rank_bm25(data:list, query:list):
    """
    rank web page with relevance to search query
    data: web pages the contain at least one search query
    query: search query
    return sorted web pages based on relevance 
    """
    bm25 = []
    for d in data:
        bm25.append(d['text'])
    bm25 = BM25Okapi(bm25)
    rank = bm25.get_scores(query)
    # add rank to web pages
    for x in range(len(data)):
        data[x]['rank'] = rank[x]
    # sort data based on rank score
    data = sorted(data, key=lambda x: x['rank'], reverse=True)
    return data
    

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

async def insert_visited_webpage(web_page:str):
    """
    Insert one web page to visited web page DB
    web_page: web page url
    """
    hash = hash_function(web_page)
    res = await crawled_link.find_one({"index":hash})
    if res:
        if web_page not in res["links"]:
            res["links"].insert(binary_insert_url(res["links"], web_page), web_page)
            response = await crawled_link.update_one({'index':hash},{'$set':{'links':res["links"]}})
            if response:
                return "Successs" 
            raise HTTPException(404, "something went wrong")
    else:
        res = await crawled_link.insert_one({"index":hash, "links":[web_page]})
        if res:
            return "Link added successfully"
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
        if link == None or '.' not in link or re.findall("\A/[a-z]", link):
            continue
        # Add https to links without https
        if re.findall("\A//", link):    
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

async def web_crawler():
    """
    Function to randomly pick web page from DB and crawl it's content
    """
    # Generate a random number between 0 and 760 both included
    index = random.randint(0, 760)
    response = await collection.find_one({"index":index})
    if response:
        # Generate a random number between 0 and len(links)
        ind = random.randint(0, len(response['links']) - 1)
        url = response['links'][ind]
        # Check if link is already visited
        res = await check_if_crawled(url)
        if res: return "Url already crawled"
        else: 
            # Get information from web page
            pg = await get_info_from_web_page(url)
            await indexing(pg)
            # Get web_links from web page
            await insert_webpages_to_db(url)
            await insert_visited_webpage(url)
            return url
    else: return "No url in index yet"

async def indexing(page:Pages):
    """
    Function to implement reverse indexing
    page: an object of Page(see model.py)
    """
    unique_text = list(dict.fromkeys(page.text))
    for token in unique_text:
        ind = await reverse_index.find_one({"index":token})
        if ind:
            ind['pages'].append(page.model_dump())
            # print(ind['pages'])
            response = await reverse_index.update_one({'index':token},{'$set':{'pages':ind['pages']}}) 
            if response:
                continue
            raise HTTPException(404, "something went wrong")
        else:
            response = await reverse_index.insert_one({"index":token, "pages":[page.model_dump()]})
            if response:
                continue
            raise HTTPException(404, "something went wrong")

async def check_if_crawled(url:str):
    """
    Function to check if url is already crawled
    """
    crawled = await crawled_link.find_one({"index":hash_function(url)})
    if crawled:
        if url in crawled["links"]:
            return True
        else: return False
    else: return False

async def clean_db():
    res = await fetch_all_webpages()
    for pages in res:
        for link in pages.links:
            if re.findall("\Ahttps:/[a-z]", link):
                print(link)
                pages.links.remove(link)
        await collection.update_one({"index":pages.index}, {'$set':{"links":pages.links}})
    print('done')


if __name__ == "__main__":
    asyncio.run(clean_db())
    # pg = asyncio.run(get_info_from_web_page("https://rccggt.org.uk"))
    # asyncio.run(indexing(pg))
    # asyncio.run(insert_webpages_to_db('https://campus.w3schools.com/collections/certifications/products/xml-certificate'))
# End-of-file (EOF)
