#!/usr/bin/env python3
import click
from source import Source
from article import Articles
from termcolor import cprint
from time import perf_counter

@click.command()
@click.option("--articles", default="download", type=str, show_default=True, help="Select option to download and parse by setting argument as 'parse'.")
@click.argument("domain", type=str)
def main(domain, articles):
    cprint(f"\u231b Building news source {domain}...", "yellow")
    t1 = perf_counter()
    paper = Source(domain)
    cprint(f"\u2713 Source successfully built in {round(perf_counter() - t1, 2)} seconds. \n", "green")

    cprint(f"\u231b Downloading articles from {len(paper.feeds)} feeds...", "yellow")
    t2 = perf_counter()
    a = Articles(paper.feeds)
    cprint(f"\u2713 Downloaded {len(a.articles)} articles in {round(perf_counter() - t2, 2)} seconds.", "green")
    tcounter = 0
    for items in a.articles:
        tcounter += 1
        if tcounter < 5:
            print(f"""
            cLink: {items.canonical_link}
            {items.title}
            by {items.authors}""")
main()