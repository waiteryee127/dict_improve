#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'

import codecs

ROOT_FILTER_PATH = "../data/filterdata/"
ROOT_ORIGINAL_PATH = "../data/originaldata/"
ROOT_SPIDER_PATH = "../data/spiderdata/"
ROOT_END_PATH = "../data/enddata/"

input_merge_dict_file = ROOT_FILTER_PATH+"merge.dic"
input_new_word_review_file = ROOT_SPIDER_PATH+"new_word.review"
input_brand_dict_file = ROOT_SPIDER_PATH+"brand.alternative"
input_kaola_brand_dict_file = ROOT_ORIGINAL_PATH+"brandInfo"

output_ecommerce_file = ROOT_END_PATH+"ecommerce.dic"
output_brand_file = ROOT_END_PATH+"brand.dic"
output_merge_dict_file = ROOT_END_PATH+"merge.dic"

merge_dict = dict()
with codecs.open(input_merge_dict_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("\t")
        if len(array) != 3:
            continue

        merge_dict[array[0]] = line
print "read merge dict end"

brand_dict = dict()
with codecs.open(input_brand_dict_file, "r", "utf-8") as f:
    for line in f:
        brand_dict[line.strip()] = 1

print "read brand dict end"

with codecs.open(input_kaola_brand_dict_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("\t")
        if len(array) != 3:
            continue

        word = array[0]
        if word not in brand_dict:
            brand_dict[word] = 1
print "read kaola brand dict end"

new_word_dict = dict()
with codecs.open(input_new_word_review_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split(":")
        if len(array) != 2:
            print line
            continue

        word = array[0]
        nature = array[1]

        if nature == "word":
            new_word_dict[word] = 1
        elif nature == "name" and word not in merge_dict:
            merge_dict[word] = word+"\t"+"nr"+"100\n"
        elif nature == "brand" and word not in brand_dict:
            brand_dict[word] = 1
print "read new word dict end"

output_merge_dict = codecs.open(output_merge_dict_file, "w", "utf-8")
for word in merge_dict:
    output_merge_dict.write(merge_dict[word])
output_merge_dict.close()
print "write merge dict end"

output_brand_dict = codecs.open(output_brand_file, "w", "utf-8")
for word in brand_dict:
    output_brand_dict.write(word+"\t"+word+"\t"+"brand\n")
output_brand_dict.close()
print "write brand end"

output_ecommerce_dict = codecs.open(output_ecommerce_file, "w", "utf-8")
for word in new_word_dict:
    output_ecommerce_dict.write(word+"\t"+"ecom\t"+"1000\n")
print "write new word end"

