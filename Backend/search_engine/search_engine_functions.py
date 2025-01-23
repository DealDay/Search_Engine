"""
    # Title    : functions for search engine
    # Filename : search_engine_functions.py
    # Author   : Adeola Ajala
"""
# Imports
import requests
from bs4 import BeautifulSoup

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

async def get_links_from_webpage(web_page_url:str):
    """
    Function to get all available links in a web page
    webPageURL: valid url
    """
    req = requests.get(web_page_url, timeout=20)
    soup = BeautifulSoup(req.text, 'html.parser')
    urls = soup.find_all('a')
    return urls

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
    pass
    