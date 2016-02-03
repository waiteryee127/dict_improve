#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'zhaobin'
import config
import codecs
import help

min_freq = 100


merge_dict = dict()
brand_dict = dict()
new_word_dict = dict()

with codecs.open(config.ROOT_FILTER_PATH+"merge.dic", "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("\t")
        if len(array) != 3:
            continue
        merge_dict[array[0]] = 1

with codecs.open(config.ROOT_SPIDER_PATH+"brand.alternative", "r", "utf-8") as f:
    for line in f:
        brand_dict[line.strip()] = 1

with codecs.open(config.ROOT_SPIDER_PATH+"new_word.review", "r", "utf-8") as f:
    for line in f:
        array = line.strip().split(":")
        if len(array) != 2:
            continue

        new_word_dict[array[0]] = 1


query_log_new_word_dict = dict()
with codecs.open(config.ROOT_ORIGINAL_PATH+"query.log", "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("\t")
        if len(array) != 2:
            continue

        freq = array[1]
        if freq.find('.') != -1:
            freq = int(freq[:freq.index('.')])
        else:
            freq = int(freq)
        if freq < min_freq:
            break

        word = array[0]
        array_word = word.split(" ")
        for w in array_word:
            if len(w) > 3 or len(w) == 1:
                continue
            if not help.is_all_chinese(w):
                continue
            if w in merge_dict or w in brand_dict or w in new_word_dict:
                continue

            if w[:2] in merge_dict or w[:2] in new_word_dict:
                continue

            query_log_new_word_dict[w] = 1

print len(query_log_new_word_dict)

output_new_word = codecs.open(config.ROOT_SPIDER_PATH+"new_word_from_log.alternative", "w", "utf-8")
for word in query_log_new_word_dict:
    output_new_word.write(word+"\n")
output_new_word.close()
