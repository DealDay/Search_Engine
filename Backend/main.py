"""
    # Title    : main backend API
    # Filename : main.py
    # Author   : Adeola Ajala
"""

# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search_engine import(
    fetch_all_webpages,
    get_links_from_webpage
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

@app.post("get_links_from_web_page")
async def get_links(web_page_url:str):
    """
        get links from web page
    """
    response = await get_links_from_webpage(web_page_url)
    return response