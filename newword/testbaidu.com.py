#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'


import urllib2

url = 'http://apis.baidu.com/apistore/pullword/words?source=暖手器&param1=0&param2=1'


req = urllib2.Request(url)

req.add_header("apikey", "4984219ad912f92c0b9830c99797e4de")

resp = urllib2.urlopen(req)
content = resp.read()
if content:
    print content
