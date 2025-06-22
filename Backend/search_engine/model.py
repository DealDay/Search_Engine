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
    title: str # web page title
    language: str # web page title
    text: list # list of words on web page

    class config:
        schema_extra={
            "example":{
                "url":"www.example.com",
                "title": "Example",
                "language": "en",
                "text": ["hello", "how", "are", "you"]
            }
        }

# class Indexing(BaseModel):
#     """Object"""
#     token: str # word
#     webPages: Pages 

#     class config:
#         schema_extra={
#             "example":{
#                 "token":"Python",
#                 "webPage": {"url":"www.example.com",
#                             "wordCount": 2,
#                             "title": "Example",
#                             "language": "en"}
#             }
#         }