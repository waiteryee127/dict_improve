#!/usr/bin/env python
# -*- coding: utf-8

__author__ = 'zhaobin'

import codecs
import config

ROOT_SPIDER_PATH = "../data/spiderdata/"
ROOT_FILTER_PATH = "../data/filterdata/"

input_file = ROOT_SPIDER_PATH+"items.j1"
input_merge_dic_file = ROOT_FILTER_PATH+"merge.dic"
input_word_from_brand_file = ROOT_SPIDER_PATH+"newwordfrombrand.firsthand"

output_word_file = ROOT_SPIDER_PATH+"word.firsthand"
output_brand_file = ROOT_SPIDER_PATH+"brand.firsthand"


def is_all_chinese(ustr):
    for uchar in ustr:
        if not is_chinese(uchar):
            return False
    return True


def is_chinese(uchar):
    if len(uchar) != 1:
        return False
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    return False


def handle_brand(brand_info):
    if brand_info.find("(") != -1:
        return brand_info[:brand_info.find("(")]
    elif brand_info.find("（") != -1:
        return brand_info[:brand_info.find("（")]
    return brand_info

brand_dict = dict()
word_dict = dict()
with codecs.open(input_file, "r", "utf-8") as f:
    num = 0
    for line in f:
        array = line.strip().split("\t")
        num += 1
        if num % 2 == 1:
            for brand in array:
                brand_cn = handle_brand(brand)
                if not is_all_chinese(brand_cn):
                    continue

                if brand_cn not in brand_dict:
                    brand_dict[brand_cn] = 1
            continue

        for word in array:
            if not is_all_chinese(word):
                continue
            for stop_word in config.filter_words:
                if stop_word in word:
                    break
            else:
                if word not in word_dict:
                    word_dict[word] = 1


brand_output = codecs.open(output_brand_file, "w", "utf-8")
word_output = codecs.open(output_word_file, "w", "utf-8")

for key in brand_dict:
    if len(key) == 0:
        continue
    brand_output.write(key)
    brand_output.write("\n")
brand_output.close()

for key in word_dict:
    if len(key) == 0:
        continue
    word_output.write(key)
    word_output.write("\n")
word_output.close()

print "get first hand new word"