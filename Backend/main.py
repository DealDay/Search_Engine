# Title    : main backend API
# Filename : main.py
# Author   : Adeola Ajala

# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search_engine import(
    fetch_all_webPages
)

# Creating instance of fastAPI
app = FastAPI()

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
@app.get("/web_pages")
async def get_web_pages():
    response = await fetch_all_webPages()
    return response