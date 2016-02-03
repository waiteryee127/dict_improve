#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'

import codecs
import config
import urllib2

brand_input_file_path = "../data/brand.firsthand"
brand_output_file_path = "../data/brand.alternative"
new_word_output_file_path = "../data/newwordfrombrand.firsthand"
filter_goods_num = -1


def fetch_new_word(keyword):
    url = config.fetch_word_by_brand_url.replace("query", keyword)
    http_request = urllib2.Request(url=url)
    http_response = urllib2.urlopen(http_request)
    html_doc = http_response.read()
    html_dict = eval(html_doc)

    extend_list = list()
    goods_num = 0
    if "extend" in html_dict:
        if "hotwords" in html_dict["extend"]:
            for value in html_dict["extend"]["hotwords"]:
                value = value.decode('unicode-escape')
                value = value.replace(keyword, "")
                extend_list.append(value)
            # extend_list = html_dict["result"]["extend"]["hotwords"]
        if "goodsnum" in html_dict["extend"]:
            goods_num = html_dict["extend"]["goodsnum"]

    if "result" in html_dict:
        for key in html_dict["result"]:
            if u"属性维度扩展" == key.decode('unicode-escape'):
                for key1 in html_dict["result"][key]:
                    for value in html_dict["result"][key][key1]:
                        extend_list.append(value.decode('unicode-escape'))

    return extend_list, goods_num


brand_file = codecs.open(brand_output_file_path, "w", "utf-8")
word_file = codecs.open(new_word_output_file_path, "w", "utf-8")
error_brand_file = codecs.open("../data/error_file", "w", "utf-8")

with codecs.open(brand_input_file_path, "r", "utf-8") as f:
    num = 0
    for line in f:
        num += 1
        if num % 200 == 0:
            print "read brand number is ", num
        brand = line.strip()
        try:
            new_word_list, num_goods = fetch_new_word(brand)

        except Exception as e:
            print e
            error_brand_file.write(brand)
            error_brand_file.write("\n")
            continue

        if int(num_goods) >= filter_goods_num:
            brand_file.write(brand)
            brand_file.write("\n")

        if len(new_word_list) == 0:
            continue

        for word in new_word_list:
            word_file.write(word)
            word_file.write("\n")

word_file.close()
brand_file.close()
