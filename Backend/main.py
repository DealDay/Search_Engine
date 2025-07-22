"""
    # Title    : main backend API
    # Filename : main.py
    # Author   : Adeola Ajala
"""

# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search_engine import (
    fetch_all_webpages,
    web_crawler,
    check_if_crawled,
    indexing,
    get_info_from_web_page,
    insert_visited_webpage

)

# Creating instance of fastAPI
app = FastAPI(openapi_version="3.0.2")

# Allow port for frontend
origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# API to get all web pages
@app.get("/web_page")
async def get_web_pages():
    """
        endpoint
    """
    response = await fetch_all_webpages()
    return response

# ApI to start automatic web crawling
@app.post("/get_links_from_web_page_to_db")
async def crawl_the_web():
    """
        start crawing web pages in the DB
    """
    response = await web_crawler()
    return response

# API to crawl info from one web page
@app.post("/crawl_web_page")
async def crawl_web_page(web_page_url:str):
    """
        crawl web page
    """
    response = await check_if_crawled(web_page_url)
    if response:
        return "Page already crawled"
    else:
        pg = await get_info_from_web_page(web_page_url)
        await indexing(pg)
        await insert_visited_webpage(web_page_url)
        return "Success"
        