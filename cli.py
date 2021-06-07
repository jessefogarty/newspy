#!/usr/bin/python3
from nuntium.migrate import OldDatabase
import argparse
import re


if __name__ == "__main__":
    years = [2018,2019,2020]
    for y in years:
        db = OldDatabase()
        db.load(y, "/home/unkwn1/projects/raw_articles.db")
        db.clean_data()
        db.migrate()
        print(db.old_data.shape)
