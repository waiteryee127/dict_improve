#!/usr/bin/env python
# -*- coding: utf-8
"""
初始过滤新词
"""

__author__ = 'zhaobin'

import codecs
import help

ROOT_SPIDER_PATH = "../data/spiderdata/"
ROOT_FILTER_PATH = "../data/filterdata/"

input_merge_dic_file = ROOT_FILTER_PATH+"merge.dic"
input_word_from_brand_file = ROOT_SPIDER_PATH+"newwordfrombrand.firsthand"
input_word_from_brand2_file = ROOT_SPIDER_PATH+"newwordfrombrand.firsthand2"
input_word_firsthand_file = ROOT_SPIDER_PATH+"word.firsthand"
input_brand_firsthand_file = ROOT_SPIDER_PATH+"brand.firsthand"
input_brand_tmall_file = ROOT_SPIDER_PATH+"tmallbrand.uniq"
input_word_tmall_file = ROOT_SPIDER_PATH+"tmallword.uniq"

output_word_file = ROOT_SPIDER_PATH+"word.alternative"
output_brand_file = ROOT_SPIDER_PATH+"brand.alternative"
output_word_dict_file = ROOT_SPIDER_PATH+"word.dict.ecommerce"


mergeDict = dict()
with codecs.open(input_merge_dic_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("\t")
        if len(array) != 3:
            continue

        mergeDict[array[0]] = 1

# 京东品牌
brandDict = dict()
with codecs.open(input_brand_firsthand_file, "r", "utf-8") as f:
    for line in f:
        brandDict[line.strip()] = 1

import jieba
newWordDic = dict()

# 天猫品牌
with codecs.open(input_brand_tmall_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("/")
        if len(array) == 2 and help.is_all_chinese(array[1]):
            brandDict[array[1]] = 1
        elif help.is_all_chinese(array[0]):
            brandDict[array[0]] = 1

print "total brand number is ", len(brandDict)


def get_new_word(line_info):
    word_alter = line_info.strip()
    if u"爷的剑" in word_alter:
        print line
    if word_alter in brandDict:
        return

    if len(word_alter) == 1:
        return

    if word_alter in mergeDict:
        newWordDic[word_alter] = 2
    elif word_alter not in mergeDict:
        if len(word_alter) < 3:
            for uchar in word_alter:
                if help.is_chinese(uchar) and word_alter not in newWordDic:
                    newWordDic[word_alter] = 1
                    break
        else:
            for idx in xrange(2, len(word_alter)):
                if word_alter[:idx] in mergeDict:
                    newWordDic[word_alter[:idx]] = 2
                    return

            word_list = jieba.cut(word_alter, cut_all=False, HMM=False)
            seg_right = False
            for seg in word_list:
                if seg in brandDict or len(seg) > 4 or len(seg) == 1:
                    continue

                seg_right = True
                if seg in mergeDict:
                    newWordDic[seg] = 2
                elif word_alter not in newWordDic:
                    newWordDic[seg] = 1

            if not seg_right:
                newWordDic[word_alter] = 1

num = 0
# 品牌扩展词以及品牌属性词
with codecs.open(input_word_from_brand_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print "read number is ", num
        if u"爷的剑" in line:
            print line,"&&&&&&&&&",num
        get_new_word(line)


# 品牌扩展词以及品牌属性词
with codecs.open(input_word_from_brand2_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print "read number is ", num
        if u"爷的剑" in line:
            print line, "%%%%%%%%%%%", num
        get_new_word(line)

# 类目属性词
with codecs.open(input_word_firsthand_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print "read number is ", num
        get_new_word(line)


# 天猫属性词
with codecs.open(input_word_tmall_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("/")
        for word in array:
            if len(word) == 1:
                continue
            get_new_word(word)

ecmo_nature = 0
new_word_num = 0
output_word = codecs.open(output_word_file, "w", "utf-8")
output_word_dict = codecs.open(output_word_dict_file, "w", "utf-8")
for word_new in newWordDic:
    if newWordDic[word_new] == 1 and help.is_all_chinese(word_new):
        output_word.write(word_new+"\n")
        new_word_num += 1
    elif newWordDic[word_new] == 2:
        output_word_dict.write(word_new+"\n")
        ecmo_nature += 1

output_word.close()
output_word_dict.close()


print "ecom number is ", ecmo_nature
print "new word number is", new_word_num

brand_output = codecs.open(output_brand_file, "w", "utf-8")
for brand in brandDict:
    brand_output.write(brand+"\n")
brand_output.close()










