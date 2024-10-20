"""Module providing schemas for DB objects"""
# Title    : DB_Model
# Filename : model.py
# Author   : Adeola Ajala
from pydantic import BaseModel

class WebPage(BaseModel):
    """Class that represent link to webpage"""
    page_link: str

    class config:
        schema_extra={
            "example":{
                "page_link":"www.example.om"
            }
        }