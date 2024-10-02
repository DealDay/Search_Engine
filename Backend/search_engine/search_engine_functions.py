# Title    : functions for search engine
# Filename : search_engine_functions.py
# Author   : Adeola Ajala

# Imports
import requests
from bs4 import BeautifulSoup

# Function to get all links in a webpage
def get_links_from_webpage(webPageURL:str):
    """
    Function to get all available links in a web page
    webPageURL: valid url
    return iterable of a tags
    """
    req = requests.get(webPageURL)
    soup = BeautifulSoup(req.text, 'html.parser')
    urls = soup.find_all('a')
    return urls

