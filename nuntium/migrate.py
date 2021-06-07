#!/usr/bin/python3

import sqlite3
from typing import Any, Mapping
from pandas import DataFrame, read_sql_query
import os
from pymongo import MongoClient  # type: ignore
import sys
from nuntium.logger import ArticleLogger
import re
import requests
from newspaper import fulltext
import lxml.html


def get_title(d) -> str:
    """Extract the title of a webpage."""
    try:
        _title = d.xpath("//meta[@property='og:title']/@content")[0]
    except IndexError:
        try:
            _title = d.xpath("//meta[@name='title']/@content")[0]
        except IndexError:
            _title = d.xpath("//title")[0].text_content()
    return _title


def get_description(d):
    """Extract the description of a webpage."""
    try:
        _desc = d.xpath("//meta[@property='og:description']/@content")[0]
    except IndexError:
        try:
            _desc = d.xpath("//meta[@name='description']/@content")[0]
        except:
            _desc = None
    return _desc


class OldDatabase:

    MONGO_URL = "mongodb://172.0.0.1"

    def __init__(self) -> None:
        """Initialize an instance of OldDatabase() with a logger."""

        self.logger = ArticleLogger("nuntium")  # initialize a logger object

        self.old_data: DataFrame

    def clean_data(self) -> None:

        self.old_data = self.old_data.drop(
            ["sub_topic", "stopwords", "ner", "source", "topic"], axis=1
        )

        for i, row in self.old_data.iterrows():

            # Request page  & store html source code
            h = requests.get(str(row["link"])).text

            doc = lxml.html.fromstring(h)

            # Redownload Article Text
            a = fulltext(h)

            # Extract meta data from OpenGraph tags

            t, d = get_title(doc), get_description(doc)

            p = doc.xpath("//meta[@property='og:site_name']/@content")

            if len(p) == 1:
                self.old_data.at[i, "source"] = p[0]

            self.old_data.at[i, "title"] = t

            self.old_data.at[i, "summary"] = d

            self.old_data.at[i, "content"] = a

            # fix date to DD/MMM/YYYY
            # eg 10/MAR/1990M
            self.old_data.at[i, "publish_date"] = re.findall(
                r"(\d+\s\w+\s\d+)", row["publish_date"]
            )[0].replace(" ", "/")

    def load(self, year: int, fp: str) -> None:
        """Load a set of old articles from a specified year.\n
        Args:
            year: int - only supports [2018,2019,2020]
            fp: str - path to sqlite3 database file\n
        Returns:
            None - adds self.old_data to the object
        """
        _fp = os.path.abspath(fp)
        self.year = year  # Set year instance var w/ input

        _con = sqlite3.connect(_fp)
        self.logger.debug(
            "Class OldDatabase() initialized with default database location %s" % (_fp)
        )

        self.old_data = read_sql_query(
            f"SELECT * FROM articles WHERE publish_date LIKE '%{self.year}%'", con=_con
        )
        self.old_data.replace("", "None", inplace=True)  # Fill empty cells
        _old_data_shape: tuple[int, int] = self.old_data.shape  # df shape for logger

        self.logger.debug(
            "Created %i articles DataFrame. Shape is %s" % (self.year, _old_data_shape)
        )

    def migrate(self) -> None:
        """Insert a DataFrame object into a specifed MongoDB.\n
        Returns:
            _mongo_result: list - list of object_id from insert_many.
        """

        try:
            _data_dict = self.old_data.to_dict(
                "records"
            )  # Convert data to list of dicts

            
            print(self.old_data)
        except:
            self.logger.critical(f"Failed to add {self.year} articles to MongoDB.")
            sys.exit
