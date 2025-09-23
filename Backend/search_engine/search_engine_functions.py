"""
    # Title    : functions for search engine
    # Filename : search_engine_functions.py
    # Author   : Adeola Ajala
"""
# Imports
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as wnl
from langdetect import detect
import asyncio
import ssl
from .model import Pages
from string import punctuation
# import motor.motor_asyncio

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('wordnet')

lang_dict = {'sq':'albanian', 'ar':'arabic', 'az':'azerbaijani', 'eu':'basque', 
             'be':'belarusian', 'bn':'bengali', 'ca':'catalan', 'zh-cn':'chinese', 
             'da':'danish', 'nl':'dutch', 'en':'english', 'fi':'finnish', 'fr':'french', 
             'de':'german', 'el':'greek', 'he':'hebrew', 'hi':'hinglish', 'hu':'hungarian', 
             'id':'indonesian', 'it':'italian', 'kk':'kazakh', 'ne':'nepali', 'no':'norwegian', 
             'pt':'portuguese', 'ro':'romanian', 'ru':'russian', 'sl':'slovene', 'es':'spanish', 
             'sv':'swedish', 'tg':'tajik', 'ta':'tamil', 'tr':'turkish'}

special_characters = list(punctuation)

def get_text_from_web_page(url:str):
    req = requests.get(url, timeout=20)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup

async def get_links_from_webpage(url:str):
    """
    Function to get all available links in a web page
    url: valid url
    """
    soup = get_text_from_web_page(url)
    urls = soup.find_all('a')
    return urls

# Function to get information from web page
async def get_info_from_web_page(url:str):
    """
    Funtion to get page title and text on a web page
    url: page url
    """
    lem = wnl()
    soup = get_text_from_web_page(url)
    if soup.title != None: page_title = soup.title.string
    else: page_title = ''
    text = soup.get_text()
    lang = detect(text)
    text = text.split()
    lem_text = []
    # set lang to en if not in lang_dict: should be revised
    if lang not in lang_dict.keys():
        lang = 'en'
    stop_words = stopwords.words(lang_dict[lang])
    for txt in text:
        if lem.lemmatize(txt).lower() not in stop_words and lem.lemmatize(txt).lower() not in special_characters:
            lem_text.append(txt.lower())
    page_info = Pages(language=lang_dict[lang], url=url, title=page_title, text=lem_text)

    return page_info

async def normalize_search_words(query:str):
    """
    Function to normaliye search words by lemmatization 
    query: search word(s)   
    """
    lem = wnl()
    # detect query language
    lang = detect(query)
    # split query
    query = query.split()
    # set lang to en if not in lang_dict: should be revised
    if lang not in lang_dict.keys():
        lang = 'en'
    stop_words = stopwords.words(lang_dict[lang])
    lem_text = []
    for txt in query:
        if lem.lemmatize(txt).lower() not in stop_words and lem.lemmatize(txt).lower() not in special_characters:
            lem_text.append(txt.lower())
    return lem_text
    
# Function to get all links in a webpage
def hash_function(value:str):
    """
    Function to produce decimal value of char.
    value: char to be coverted to decimal
    returns tuple of decimal value and decimal value mod 761(decimal value of char(https:// and .)
    """
    sum_of_chars = 0
    for char in value:
        sum_of_chars += ord(char)

    return sum_of_chars % 761

def string_to_binary(txt_value:str):
    """
        Function to convert text to binary
        Value: text to converted
        returns binary
    """
    bin = ''.join(format(ord(i), '08b') for i in txt_value)
    return bin
    
def binary_to_string(bin_value:str):
    """
        Function to convert binary to text
        Value: bin to converted
        returns text
    """
    text = ''
    # slicing the input and converting it
    for i in range(0, len(bin_value), 8):
        # collecting 1byte of data to convert to string
        temp_bin = bin_value[i:i+8]
        # convert bin to dec
        dec_val = int(temp_bin, 2)
        # append it to text
        text = text + chr(dec_val)
    return text

def binary_insert_url(arr, targetVal):
    """
        function to return insert index for a url using binary value of url
        to sort.
        arr: array of urls
        targetVal: url to be inserted
    """
    left = 0
    right = len(arr) - 1
    if right == 0:
        if string_to_binary(arr[right]) < string_to_binary(targetVal):
            return right + 1
        else: return right

    while left < right:
        if string_to_binary(arr[right]) < string_to_binary(targetVal):
            return right + 1
            break
        if string_to_binary(arr[left]) > string_to_binary(targetVal):
            return left
            break
        mid = (left + right) // 2 
        if string_to_binary(arr[mid]) < string_to_binary(targetVal):
            left = mid + 1
        else: 
            right = mid - 1
    return left

if __name__ == "__main__":
    # get_info_from_web_page("https://www.tutorialspoint.com/extract-the-title-from-a-webpage-using-python#:~:text=The%20urllib%20and%20BeautifulSoup%20method,title'%20attribute.")
    pg = asyncio.run(get_info_from_web_page("https://rccggt.org.uk"))
    # print(pg.text)
    # pass
    