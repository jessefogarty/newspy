#!/usr/bin/env python3
'''
Nuntium parsers for new articles.

This module contains functions and classes to parse news articles from various sources. 
'''

import asyncio
import re
import extruct
import json

class SchemaParser():

    def __init__(self, data):
        self._data = self._read_in(data)
        self.tags = self.run()

    def run(self):
        return asyncio.run(self.find_tags(self._data))
    def _read_in(self, data):
        return extruct.extract(
                data,
                syntaxes=["json-ld"], uniform=True
                )["json-ld"][0]

    async def _parse_tag(self, sdict:dict):
        _tag = {}
        _child_tags = []
        _type = sdict.get("@type")
        if type(_type) is list:
            _type = ",".join(_type)
        _tag["@type"] = _type
        for k,v in sdict.items():
            #print(k, "-", type(v)
            
            if type(v) is str:
                if "@" not in k:
                    _tag[k] = v
            elif type(v) is dict:
                _child_tags.append(v)
        return _tag, _child_tags

    async def find_tags(self, data):
        _tags = []
        _tag, _children = await self._parse_tag(self._data)
        _tags.append(_tag)
        if len(_children) > 0:
            for child in _children:
                _tag, _ = await self._parse_tag(child)
                _tags.append(_tag)
        return _tags


