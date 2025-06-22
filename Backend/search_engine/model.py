"""Module providing schemas for DB objects"""
# Title    : DB_Model
# Filename : model.py
# Author   : Adeola Ajala
from pydantic import BaseModel

class WebPage(BaseModel):
    """Class that represent link to webpage"""
    links: list
    index: int

    class config:
        schema_extra={
            "example":{
                "links":"www.example.com",
                "index": "compute by hash algorith"
            }
        }

class Pages(BaseModel):
    """Object of web page"""
    url: str # url of web page
    wordCount: int # how many times a word appear on the web page
    title: str # web page title

    class config:
        schema_extra={
            "example":{
                "url":"www.example.com",
                "wordCount": 2,
                "title": "Example"
            }
        }

class Indexing(BaseModel):
    """Object"""
    token: str # word
    webPages: Pages 

    class config:
        schema_extra={
            "example":{
                "token":"Python",
                "webPage": {"url":"www.example.com",
                            "wordCount": 2,
                            "title": "Example"}
            }
        }