#!/usr/bin/python3
from nuntium.migrate import OldDatabase
import argparse

"""
cli = argparse.ArgumentParser()
cli.add_argument("year", help="Select a year (of articles) to import", type=int)
cli_args = cli.parse_args()
year = cli_args.year
if year not in [2018, 2019, 2020]:
    raise ValueError(f"Input Must Be: 2018, 2019, 2020.")
db = OldDatabase()
db.migrate(year)"""


if __name__ == "__main__":
    db = OldDatabase()
    db.load(2019, "nuntium/raw_articles.db")
    db.migrate()