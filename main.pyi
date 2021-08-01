from concurrent.futures import ThreadPoolExecutor as ThreadPoolExecutor
from pandas import DataFrame as DataFrame, read_sql_query as read_sql_query
from time import sleep as sleep
from typing import Any

go_parser: str
years: Any
con: Any
articles: Any
cur: Any
article_list: Any
links: Any
str_links: Any
html: Any
h: Any
doc: Any
