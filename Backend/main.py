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
    get_links_from_webpage,
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

@app.post("/get_links_from_web_page_to_db")
async def get_links(web_page_url:str):
    """
        get links from web page
    """
    response = await get_links_from_webpage(web_page_url)
    return response

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
        