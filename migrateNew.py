#!/usr/bin/python3

import sqlite3
from typing import Any, Mapping
from pandas import DataFrame, read_sql_query
import os
import subprocess
from pymongo import MongoClient  # type: ignore
import sys
import re
import requests
from newspaper import fulltext
import lxml.html
from concurrent.futures import ThreadPoolExecutor
from time import sleep


go_parser = "/home/unkwn1/GitHub/Python/nuntium/nuntium/gghtml"

years = [2018]

con = sqlite3.connect("/home/unkwn1/Documents/raw_articles.db")
articles = {}

for y in years:
    cur = con.cursor()
    _d = cur.execute(
        f"SELECT link, publish_date, authors FROM articles WHERE publish_date LIKE '%{y}%'"
    ).fetchall()
    article_list = []
    links = [l[0] for l in _d]
    str_links = ",".join(l for l in links)


    html = subprocess.run([go_parser, str_links], stdout=subprocess.PIPE)
    print(html.stdout)
"""
    for i, d in enumerate(_d):

        _article: dict = {}
        h = requests.get(d[0]).text
        doc = lxml.html.fromstring(h)

        _article["authors"] = d[2]
        _article["publish_date"] = re.findall(r"(\d+\s\w+\s\d+)", d[1])[0].replace(
            " ", "/"
        )
        _article["text"] = fulltext(h)
        _article["source"] = doc.xpath("//meta[@property='og:site_name']/@content")[0]
        _article["summary"] = doc.xpath("//meta[@property='og:description']/@content")[
            0
        ]
        _article["title"] = doc.xpath("//meta[@property='og:title']/@content")[0]
        article_list.append(_article)

    articles[y] = article_list

    _mongo: MongoClient = MongoClient("localhost", 27017)  # Connect to DB
    _mongo_db = _mongo["articles"]  # Init DB
    _mongo_collection = _mongo_db[f"from_{y}"]  # init collection
    _mongo_collection.insert_many(article_list)
"""
