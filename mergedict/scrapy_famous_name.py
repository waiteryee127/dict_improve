#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'

"""
解析大陆及港台明星姓名
"""

input_file_DL = "../data/originaldata/famous_name_china"
input_file_GT = "../data/originaldata/famous_name_GT"

output_famous_name = "../data/filterdata/famous_name"

import codecs

html = ""
with codecs.open(input_file_DL, "r", "utf-8") as f:
    for line in f:
        html += line

with codecs.open(input_file_GT, "r", "utf-8") as f:
    for line in f:
        html += line

from lxml import etree
tree = etree.HTML(html)
nodecs = tree.xpath("//a/text()")

from newword import help
output_famous = codecs.open(output_famous_name, "w", "utf-8")
for node in nodecs:
    if len(node) > 4:
        continue
    if not help.is_all_chinese(node):
        continue
    output_famous.write(node+"\n")

output_famous.close()
