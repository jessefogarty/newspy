#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import lxml.html
from newspaper import fulltext

class Article():
    def __init__(self, url:str = "", title:str = "", summary:str = "", authors:list[str] = [], publish_date:str = "", text:str = "") -> None:
        self._url = url
        self._title = title
        self._summary = summary
        self._authors = authors
        self._publish_date = publish_date
        self._text = text