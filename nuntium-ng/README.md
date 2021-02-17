# Nuntium
A somewhat intelligent parser for news sources and their articles.


## Current Features 

**Source()** - an object containing the basic information; title, description and, found feeds.

**Articles()** - Finds new articles from a provided list of RSS/Atom feeds.

### TODO:
- remove self.feeds from Articles - retrieve should take arg
- Store Source() + Artices() objects in an SQLite database.
    - check for stored data *before* running.
- initial article parsing
- make extractors.meta_data() more modular **Non-Priority**
 
---
## Usage

### CLI Syntax
```python
from source import Source
from article import Articles
python3 nuntium.py <domain> --articles <'download'/'parse'>
```

### Building a Source
```python
from source import Source
from extractors import meta_data
paper = Source('domain')
# Source functions - called during __init__
.find_feeds()
.meta_data()
# Source properties
.homepage: str
.title: str
.description: str
.feeds: list
```

### Building Articles
```python
from article import Articles
articles = Articles([feeds])
# Articles functions - called during __init__
.retrieve()
.download()
# Articles properties
.article_list: list, str
.articles: list, dict
```