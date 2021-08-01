# Nuntium

> A tool to migrate an old news database from sqlite -> mongo

![Python - Type & Coding Checks](https://github.com/jessefogarty/nuntium/actions/workflows/python_alphaChecks.yml/badge.svg?branch=old-database&event=push)](https://github.com/jessefogarty/nuntium/actions/workflows/python_alphaChecks.yml)
![Python3](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%20|%203.9-green)


Nuntium was initially started as a news scraping project. Created and run mainly during 2019, the databse grew to over 150,000 articles from Canadian news outlets. As my idea for the project changed so to did nuntium.

## Prerequisites / Notices

- An sqlite database. A sample is provided.
- A mongodb server. Built around a docker container.
- **Only tested on Arch Linux using Python 3.9**
  - Please let me know if you test it on anything else :).

---

## Installing Nuntium

`git clone https://github.com/jessefogarty/nuntium.git && cd nuntium`

`pip install -r requirements.txt`

Download sample database from Kaggle (**TODO**)

## Example Usage of Nuntium

*Please refer to code in `test/nuntium_dev.py`*

## TODO

>*likely to be added as issues to hold myself accountable*

- Test entire DB migration
- Create sample dataset from raw_articles.db
  - upload to kaggle; update readme with link
- Create archived backup of MongoDB container
- Setup.py? Meh.

### Contributing & License

Idk why you would want. But, in the event someone does please fell free to submit a PR with a few brief bullet poins explaining any changes.

The code is free. Do whatever you please and remember to ***give credit where credit is due***.
