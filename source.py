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

CBC_RSS = ["https://rss.cbc.ca/lineup/world.xml","https://rss.cbc.ca/lineup/topstories.xml"]




class Source():

    def __init__(self, homepage:str = "", feeds:list[str] = []) -> None:
        self._homepage = homepage
        self._feeds = ["https://rss.cbc.ca/lineup/world.xml","https://rss.cbc.ca/lineup/topstories.xml"]
        self._new_articles: list[tuple[str, str]]= [] # list of tuples (url, html)

    def update(self):
        '''
        Update the source
        '''
        asyncio.run(self.get_new_articles())

    async def get_new_articles(self, save=True) -> list[str]:
        '''
        Read the rss feeds and return a list of html sources for each article
        '''
        async def _read_feed(feed_url):
            '''
            Read the feed and return a list of links
            '''
            _, _html = await download(feed_url, _session)
            soup = bs(_html, "lxml-xml")
            links = [link.text for link in soup.find_all("link")][2:]
            return links
        async with aiohttp.ClientSession() as _session:
            _article_urls = await asyncio.gather(*[_read_feed(url) for url in self._feeds])      
            articles = [await asyncio.gather(*[download(link, _session) for link in feed]) for feed in _article_urls]
            if save != True:
                return articles
            self._new_articles = articles

if __name__ == "__main__":
    _source = Source()
    #_data = asyncio.run(_source.get_new_articles(save=False))
    _source.update()
    print(_source.__dict__)
