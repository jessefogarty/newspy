#!/usr/bin/env python3
'''
Nuntium parsers for new articles.

This module contains functions and classes to parse news articles from various sources. 
'''

import asyncio
import re
import extruct
import json

async def SchemaParser(html:str) -> list:

    async def _parse_tag(sdict:dict):
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
    
    async def _find_tags(_data):
        _tags = []
        _tag, _children = await _parse_tag(_data)
        _tags.append(_tag)
        if len(_children) > 0:
            for child in _children:
                _tag, _ = await _parse_tag(child)
                _tags.append(_tag)
        return _tags

    _data = extruct.extract(
                html,
                syntaxes=["json-ld"], uniform=True
                )["json-ld"][0]
    _tags = await _find_tags(_data)
    return _tags 



