#!/usr/bin/env python3

import lxml.html
import requests


def meta_data(h:str, *argv) -> list:
    '''Extract meta data of a webpage from the html.
    '''
    data = []
    doc = lxml.html.fromstring(h)

    def title(d) -> str:
        '''Extract the title of a webpage.'''
        try:
            _title = d.xpath("//meta[@property='og:title']/@content")[0]
        except IndexError:
            try:
                _title = d.xpath("//meta[@name='title']/@content")[0]
            except IndexError:
                _title = d.xpath("//title")[0].text_content()
        return _title
    
    def description(d):
        '''Extract the description of a webpage.'''
        try:
            _desc = d.xpath("//meta[@property='og:description']/@content")[0]
        except IndexError:
            try:
                _desc = d.xpath("//meta[@name='description']/@content")[0]
            except:
                _desc = None
        return _desc

    for arg in argv:
        arg.lower()
        if arg == 'title':
            data.append(title(doc))
        elif arg == 'description':
            data.append(description(doc))
        else:
            raise ValueError(f'{arg} cannot be parsed.')

    return data


if __name__ == "__main__":
    urls = ["https://cbc.ca", "https://cnn.com", "http://thestar.com", "https://torontosun.com"]

    for url in urls:
        r = requests.get(url)
        h = r.content
        print(meta_data(h, "title", "description"))
