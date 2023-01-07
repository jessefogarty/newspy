import asyncio
from article import Article
import requests
import extruct
import aiohttp
import json
from utils import SchemaParser

async def test1():
    _url = "https://www.cbc.ca/news/world/iran-nuclear-deal-1.6031550"; _html = requests.get(_url).text
    _article = Article(_url, _html)
    return await _article.parse()

async def test2():
    _url = "https://www.thestar.com/news/world/americas/2023/01/04/us-reopening-visa-and-consular-services-at-embassy-in-cuba.html"; _html = requests.get(_url).text
    _article = Article(_url, _html)
    return await _article.parse()
async def test3():
    _url = "https://www.theguardian.com/world/2023/jan/06/six-journalists-reportedly-held-over-footage-of-south-sudans-president-wetting-himself"; _html = requests.get(_url).text
    _article = Article(_url, _html)
    return await _article.parse()

async def schema_parser(html) -> dict:
    return extruct.extract(
                html,
                syntaxes=["json-ld"], uniform=True
                )

async def get_schema_type(schema_dict, type:str):
    for key in schema_dict:
        if len(schema_dict[key]) > 0:
            for item in schema_dict[key]:
                if item[skey] == sval:
                    return item

async def schema_test(url, name):
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            #_schema_data = await schema_parser(await response.text())

            _schema = SchemaParser(await response.text())
            print(_schema.tags)
                #print(_schema_data
            #with open(f"./tests/test-{name}.json", "w") as f:
                #json.dump(_schema_data, f, indent=4)
    #print(await get_schema_tag(_schema_data, "@type", "NewsMediaOrganization"))

async def run_tests():
    print(await asyncio.gather(test1(), test2()))

if __name__ == "__main__":
    urls= [("https://www.cbc.ca/news/world/iran-nuclear-deal-1.6031550", "cbc"), ("https://www.torontosun.com/news/world/2023/01/04/iran-says-it-will-continue-to-enrich-uranium-despite-us-sanctions", "torsun"), ("https://www.thestar.com/news/world/americas/2023/01/04/us-reopening-visa-and-consular-services-at-embassy-in-cuba.html", "star")]
    for url, name in urls:
        asyncio.run(schema_test(url, name))