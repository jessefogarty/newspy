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
from network import download_html
from article import Article
from utils import SchemaParser

CBC_RSS = ["https://rss.cbc.ca/lineup/world.xml","https://rss.cbc.ca/lineup/topstories.xml"]




class Source():

    def __init__(self, homepage:str = "", feeds:list[str] = []) -> None:
        self._homepage = homepage
        self._feeds = ["https://rss.cbc.ca/lineup/world.xml","https://rss.cbc.ca/lineup/topstories.xml"]
        self._last_fetch_urls: list= [] # list of tuples (url, html)
        self._last_fetch_articles = []

    async def update(self, fetch_articles:bool = True):
        '''
        Update the source
        '''
        async def _read_feed(feed_url, session):
            '''
            Read the feed and return a list of links
            '''
            try:
                _html = await download_html(feed_url, session)
                soup = bs(_html, "lxml-xml")
                links = [link.text for link in soup.find_all("link")][2:]
                return links
            except:
                logging.error(f"Failed to read feed: {feed_url}")
                return []

        async with aiohttp.ClientSession() as _session:
            for feed in self._feeds:
                self._last_fetch_urls.extend(await _read_feed(feed, _session))
            with self.download_articles(_session) as _article:
            for url in self._last_fetch_urls:
                _html = await download_html(url, _session)
                _article = Article(url, _html)
                await _article.parse()
                self._last_fetch_articles.append(_article)


    async def download_articles(self, session):
        '''
        Read the rss feeds and return a list of html sources for each article
        '''
        for url in self._last_fetch_urls:
                _html = await download_html(url, session)
                _article = Article(url, _html)
                await _article.parse()
                yield _article

        
    

if __name__ == "__main__":
    _source = Source()
    #_data = asyncio.run(_source.get_new_articles(save=False))
    asyncio.run(_source.update())
    print(_source._last_fetch_articles[0].__dict__)
    #print(_source._new_articles)
    #for article in _source._new_articles:
        #for url, html in article:
            #_a = Article(url, html)
            #asyncio.run(_a.parse())
            #print(_a.__dict__.get("_summary"))
            #print(asyncio.run(SchemaParser(html)))
            #_d = SchemaParser(html)
            #print(await _d.run())
            #print(_d.tags)