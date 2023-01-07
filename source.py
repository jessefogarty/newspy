#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A newspaper source object
'''
import asyncio
import aiohttp
import logging
import os
from bs4 import BeautifulSoup as bs
import time
from network import download
from article import Article
from utils import SchemaParser

CBC_RSS = ["https://rss.cbc.ca/lineup/world.xml","https://rss.cbc.ca/lineup/topstories.xml"]




class Source():

    def __init__(self, homepage:str = "", feeds:list[str] = []) -> None:
        self._homepage = homepage
        self._feeds = ["https://rss.cbc.ca/lineup/world.xml","https://rss.cbc.ca/lineup/topstories.xml"]
        self._new_articles: list[tuple[str, str]]= [] # list of tuples (url, html)

    async def update(self):
        '''
        Update the source
        '''
        async with aiohttp.ClientSession() as _session:
            self._new_articles = await self.get_new_articles(_session)


    async def get_new_articles(self, session) -> list:
        '''
        Read the rss feeds and return a list of html sources for each article
        '''
        async def _read_feed(feed_url):
            '''
            Read the feed and return a list of links
            '''
            _, _html = await download(feed_url, session)
            soup = bs(_html, "lxml-xml")
            links = [link.text for link in soup.find_all("link")][2:]
            return links

        _article_urls = await asyncio.gather(*[_read_feed(url) for url in self._feeds])      
        articles: list = [await asyncio.gather(*[download(link, session) for link in feed]) for feed in _article_urls]
        return articles

if __name__ == "__main__":
    _source = Source()
    #_data = asyncio.run(_source.get_new_articles(save=False))
    asyncio.run(_source.update())
    for article in _source._new_articles:
        for url, html in article:
            print(SchemaParser(html).run())