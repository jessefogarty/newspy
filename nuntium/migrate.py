#!/usr/bin/python3

import sqlite3
from time import strptime
from pymongo import MongoClient  # type: ignore
import re
import requests
import subprocess
from newspaper import fulltext
import lxml.html
from datetime import datetime
import json


years = [2018]

con = sqlite3.connect("/home/unkwn1/projects/raw_articles.db")

for y in years:
    cur = con.cursor()
    _d = cur.execute(
        f"SELECT link, publish_date, authors FROM articles WHERE publish_date LIKE '%{y}%'"
    ).fetchall()
    # article_list = []

    urls = [l[0] for l in _d]
    strUrls = ",".join(str(elem) for elem in urls)
    htmls = subprocess.run(
        ["/home/unkwn1/projects/github/nuntium/nuntium/gghtml", f"{strUrls}"],
        stdout=subprocess.PIPE,
        text=True,
    )
    print(json.loads(htmls.stdout))
"""
    for io, d in enumerate(_d):
        
        _article: dict = {}
        try:
            r = requests.get(d[0])
        except:
            continue
        # If not valid html doc found skip
        try:
            doc = lxml.html.fromstring(r.text)
        except:
            continue

        _article["url"] = r.url # absolute url no query str
        _article["authors"] = str(d[2]).split(", ") # split author string, store as array
        _article["publish_date"] = re.findall(r"(\d+\s\w+\s\d+)", d[1])[0].replace(
            " ", "/"
        ) # converting time format from original
        _article["publish_date"] = datetime.strptime(
            _article["publish_date"], "%d/%b/%Y"
        ) # date stored as ISODate() in Mongo
        _article["text"] = fulltext(r.text) # Use newspaper3k function to get article text from html
        
        try:
            _article["source"] = doc.xpath("//meta[@property='og:site_name']/@content")[
                0
            ]
        except:
            pass

        try:
            _article["summary"] = doc.xpath(
                "//meta[@property='og:description']/@content"
            )[0]
        except IndexError:
            pass
        try:
            _article["summary"] = doc.xpath("//meta[@name='description']/@content")[
                0
            ]
        except IndexError:
            continue

        try: # Title from opengraph tag
            _article["title"] = doc.xpath("//meta[@property='og:title']/@content")[0]
        except IndexError:
            try: # Title from meta tag
                _article["title"] = doc.xpath("//meta[@name='title']/@content")[0]
            except IndexError:
                try: # Title from title html tag
                    _article["title"] = doc.xpath("//title")[0].text_content()
                except:
                    continue

        article_list.append(_article)

    _mongo: MongoClient = MongoClient("localhost", 27017)  # Connect to DB
    _mongo_db = _mongo["articles"]  # Init DB
    _mongo_collection = _mongo_db[f"from_{y}"]  # init collection
    _mongo_collection.insert_many(article_list)
"""
