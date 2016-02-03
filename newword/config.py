#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'

filter_words = [u"的", u"很", u"效果"]

domain = "http://172.17.3.216:51355"
fetch_word_by_brand_url = domain+"/newword?keyword=query"
fetch_word_by_brand_url_new = domain+"/extend?brand=query1&category=query2&title=query3"

ROOT_ORIGINAL_PATH = "../data/originaldata/"
ROOT_FILTER_PATH = "../data/filterdata/"
ROOT_SPIDER_PATH = "../data/spiderdata/"

