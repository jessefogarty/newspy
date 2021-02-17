#%%
import re
import time
import requests
import lxml.html
from extractors import meta_data

class Source():
    def __init__(self, d:str):
        # Strip http/s + create .domain var
        resp = requests.get(d)
        
        self.homepage = resp.url

        self.feeds = self.find_feeds()

        self.title, self.description = meta_data(resp.content, "title", "description")
        
    def __repr__(self):
        rep = f"The Source({self.homepage}) contains \n {self.__dict__}"
        return rep

    def find_feeds(self) -> list:
        """Try to find the feed(s) of a website from a homepage url.\n
        Args:\n
            url(str) - Homepage url. Use requests response.url preferrably.\n
        Returns:\n
            feedlinks(list) - a list of found feeds.
        """
        # find source RSS feed(s); add to source {}.
        def _extract_links(h:str) -> list:
            """Extracts rss|xml links from html.
            Args:
                h(str) - the html of a webpage in a string.
            Returns:
            
            """
            data = lxml.html.fromstring(h)
            # create a list of all links from html
            all_links = data.xpath("//a/@href")
            # create a list of (feed) urls ending in .xml or .rss
            # TODO: fix regex for .rss
            feed_urls = []
            [feed_urls.append(f) for f in all_links if re.search(r"\.(xml|rss)$", f) and f not in feed_urls]

            return feed_urls

        feed_links = []

        _feed_url = self.homepage + "feed"

        _feed_response = requests.get(_feed_url)

        # try _rss_url if _feed_url return a 404
        if _feed_response.status_code == 404:
            # Create _url/rss & Request RSS URL
            _rss_url = self.homepage + "rss"
            _rss_response = requests.get(_rss_url)
            # if response is application return response.url
            if (
                _rss_response.status_code == 200
                and "application" in _rss_response.headers["Content-Type"]
            ):
                feed_links.append(_rss_response.url)
            # if response is text try to extract rss links from webpage
            elif (
                _rss_response.status_code == 200
                and "text" in _rss_response.headers["Content-Type"]
            ):
                feed_links = _extract_links(_rss_response.content)

        elif _feed_response.status_code == 200:
            # if response is application return response.url
            if "application" in _feed_response.headers["Content-Type"]:
                feed_links.append(_feed_response.url)
            # if response is text try to extract rss links from webpage
            elif "text" in _feed_response.headers["Content-Type"]:
                feed_links = _extract_links(_feed_response.content)

        return feed_links

if __name__ == "__main__":
    tests = ["https://cbc.ca", "https://nationalpost.com", "https://cnn.com"]

    for test in tests:
        print(f"Building Source {test}...") 
        start_time = time.perf_counter()    
        f = Source(test)
        fin_time = time.perf_counter() - start_time 
        print(f)
        
        print(f"finished building source in {round(fin_time, 2)} sec. \n")  


