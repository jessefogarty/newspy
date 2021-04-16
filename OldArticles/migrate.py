#!/usr/bin/python3

# %% Imports Cell
import sqlite3
from pandas import read_sql_query  # type: ignore
import os
from pandas.core.frame import DataFrame  # type: ignore
from logger import ArticleLogger
from pymongo import MongoClient  # type: ignore
import sys

#%% OldDatabase Definitions Cell
class OldDatabase:

    FILE_NAME = os.path.abspath("raw_articles.db")

    MONGO_URL = "mongodb://172.17.0.2"

    def __init__(self) -> None:
        """ Initialize an instance of OldDatabase() with a logger."""

        self.logger = ArticleLogger("OldDatabase")  # initialize a logger object
        self.logger.debug(
            "Class OldDatabase() initialized with default database location %s"
            % (OldDatabase.FILE_NAME)
        )
        self.year: int
        self.old_data: DataFrame

    def load(self, year: int) -> None:
        """Load a set of old articles from a specified year.\n
        Args:\n
            year: int - only supports [2018,2019,2020]\n
        Object:\n
            self.old_data: DataFrame
        """

        self.year = year  # Set year instance var w/ input

        _con = sqlite3.connect(OldDatabase.FILE_NAME)
        self.old_data = read_sql_query(
            f"SELECT * FROM articles WHERE publish_date LIKE '%{self.year}%'", con=_con
        )

        self.old_data.replace("", "None", inplace=True)  # Fill empty cells
        _old_data_shape: tuple[int, int] = self.old_data.shape  # df shape for logger

        self.logger.debug(
            "Created %i articles DataFrame. Shape is %s" % (self.year, _old_data_shape)
        )

    def migrate(self, df: DataFrame) -> None:

        if self.year is int and [2018, 2019, 2020]:  # check for supported years
            _data_dict: list = self.old_data.to_dict(
                "records"
            )  # Convert data to list of dicts

            _mongo: MongoClient = MongoClient(
                "mongodb://172.17.0.2:27017"
            )  # Connect to DB
            _mongo_db = _mongo["articles"]  # Init DB
            _mongo_collection = _mongo_db[f"from_{self.year}"]  # init collection
            _mongo_collection.insert_many(_data_dict)
        else:
            self.logger.critical(f"Failed to add {self.year} articles to MongoDB.")
            sys.exit


#%% Test Cell
test = OldDatabase()
test.load(2018)

#%%


# %%
"""
if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("year", help="Select a year (of articles) to import", type=int)
    cli_args = cli.parse_args()
    year = cli_args.year
    if year not in [2018, 2019, 2020]:
        raise ValueError(f"Input Must Be: 2018, 2019, 2020.")
    db = OldDatabase()
    db.migrate(year)
"""