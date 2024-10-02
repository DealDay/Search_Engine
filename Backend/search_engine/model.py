# Title    : DB_Model
# Filename : model.py
# Author   : Adeola Ajala
from pydantic import BaseModel

class WebPage(BaseModel):
    page_link: str

    class config:
        schema_extra={
            "example":{
                "page_link":"www.example.om"
            }
        }