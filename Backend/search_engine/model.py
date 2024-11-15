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
                "links":"www.example.om",
                "index": "compute by hash algorith"
            }
        }