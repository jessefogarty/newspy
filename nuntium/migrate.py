#!/usr/bin/python3

import sqlite3
from typing import Any, Mapping
from pandas import DataFrame, read_sql_query
import os
from pymongo import MongoClient  # type: ignore
import sys
from nuntium.logger import ArticleLogger


class OldDatabase:

    MONGO_URL = "mongodb://172.17.0.2"

    def __init__(self) -> None:
        """ Initialize an instance of OldDatabase() with a logger."""

        self.logger = ArticleLogger("nuntium")  # initialize a logger object

        self.old_data: DataFrame

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

            _mongo: MongoClient = MongoClient(
                "mongodb://172.17.0.2:27017"
            )  # Connect to DB
            _mongo_db = _mongo["articles"]  # Init DB
            _mongo_collection = _mongo_db[f"from_{self.year}"]  # init collection
            _mongo_collection.insert_many(_data_dict)
        except:
            self.logger.critical(f"Failed to add {self.year} articles to MongoDB.")
            sys.exit
