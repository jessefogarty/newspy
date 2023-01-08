#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import lxml.html
import requests
from newspaper import fulltext
import re
from prettytable import PrettyTable as pt
from network import download_html
from utils import SchemaParser
class Article():
    def __init__(self, url:str, html:str, title:str = "", summary:str = "", authors:list[str] = [], publish_date:str = "", text:str = "") -> None:
        self._url = url
        self._html = html
        self._schema_tags:list = []
        self._title = title
        self._summary = summary
        self._authors = authors
        self._publish_date = publish_date
        self._text = text
    
    def __repr__(self) -> str:
        return f"""Article({self._title}, 
        {self._publish_date}, 
        {self._url},)"""
    async def download(self):
        '''
        Download the article
        '''
        async with aiohttp.ClientSession() as _session:
            self._html = await download_html(self._url, _session)
    async def parse(self):
        '''
        Parse the article
        '''
        self._schema_tags = await SchemaParser(self._html)
        _doc = lxml.html.fromstring(self._html)
        self._title = await self._get_title(_doc)
        self._publish_date = await self._get_publish_date(_doc)
        self._summary = await self._get_summary()
        #self._authors = await self._get_authors(_doc)
        try:
            self._text = await self._get_text()
        except:
            pass

    async def _get_summary(self):
        '''
        Get the summary
        '''
        if len(self._schema_tags) > 0:
            for tag in self._schema_tags:
                try:
                    return tag["description"]
                except:
                    pass
            #return self._schema_tags.get("description")

    async def _get_text(self):
        '''
        Get the text
        '''
        return fulltext(self._html)
    
    async def _get_publish_date(self, _doc):
        '''
        Get the publish date
        '''
        return _doc.find(".//time").text

    async def _get_title(self, _doc):
        '''
        Get the title
        '''
        return _doc.find(".//title").text
    async def _get_authors(self, _doc):
        '''
        Get the authors
        '''
        return _doc.find(".//author").text




if __name__ == "__main__":
    pass