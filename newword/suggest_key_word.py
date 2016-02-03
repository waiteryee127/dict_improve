#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'

import xlrd
import urllib2
import config
import xlwt

input_file = u"../data/originaldata/各类目无搜索标签列表20151204.xlsx"
output_file = u"../data/originaldata/各类目无搜索标签列表20151204_.xls"

data = xlrd.open_workbook(input_file)

table = data.sheets()[0]

nrows = table.nrows
ncols = table.ncols

xlw = xlwt.Workbook()
table_w = xlw.add_sheet('keyword', cell_overwrite_ok=True)

col_field_name_dict = dict()

for idx in xrange(0, ncols):
    col_field_name_dict[table.cell(0, idx).value] = idx
    table_w.write(0, idx, table.cell(0, idx).value)
table_w.write(0, ncols+1, u"keyword")


def fetch_keyword(brand_info, category_info, title_info):
    url = ""
    if brand_info != "NONE":
        url = config.fetch_word_by_brand_url_new.replace("query1", brand_info)\
            .replace("query2", category_info).replace("query3", "")
    elif title_info != "NONE":
        url = config.fetch_word_by_brand_url_new.replace("query1", "")\
            .replace("query2", "").replace("query3", title_info)

    key_words_list = list()

    http_request = urllib2.Request(url=url)
    http_response = urllib2.urlopen(http_request)
    html_doc = http_response.read()
    html_dict = eval(html_doc)
    if html_dict["code"] == "400":
        return key_words_list

    for key in html_dict["result"]:
        if u"相关词扩展" == key.decode('unicode-escape'):
            for value in html_dict["result"][key]:
                key_words_list.append(value.decode('unicode-escape'))
                if len(key_words_list) == 20:
                    break

            break

    return key_words_list


for row in xrange(1, nrows):
    if row % 100 == 0:
        print row
    title = table.cell(row, col_field_name_dict[u"商品名称"]).value
    brand = table.cell(row, col_field_name_dict[u"品牌"]).value
    lei_mu = table.cell(row, col_field_name_dict[u"叶子类目名称"]).value

    for idx in xrange(0, ncols):
        table_w.write(row, idx, table.cell(row, idx).value)

    try:
        words_list = fetch_keyword("NONE", "NONE", lei_mu)
        if len(words_list) == 0:
            words_list = fetch_keyword(title, brand, "NONE")
    except Exception as e:
        print e
        print title, brand, lei_mu
        try:
            words_list = fetch_keyword(title, brand, "NONE")
        except Exception as e:
            print e
            print title, brand, lei_mu
            continue

    key_words = ";".join(words_list)
    table_w.write(row, ncols+1, key_words)


xlw.save(output_file)
