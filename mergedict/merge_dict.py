#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'

"""
将ansj中的core.dic、default.dic和hanlp的CoreNatureDictionary.txt
以及jieba的dict.txt四个词典文件进行合并。
"""

import codecs

wordDic = dict()

ROOT_PATH = "../data/originaldata/"
ROOT_END_PATH = "../data/enddata/"

merge_dict_file = ROOT_PATH+"merge.dic"
ansj_dict_default_file = ROOT_PATH+"default.dic"
ansj_dict_core_file = ROOT_PATH+"core.dic"
hanlp_dict_file = ROOT_PATH+"CoreNatureDictionary.txt"
jieba_dict_file = ROOT_PATH+"dict.txt"
ansj_basic_file = ROOT_END_PATH+"basic.dic"

hanlp_extend_word = codecs.open("../data/hanlp_extend_word.dic", "w", "utf-8")
ansj_exetnd_word = codecs.open("../data/ansj_extend_word.dic", "w", "utf-8")
ansj_basic_word = codecs.open(ansj_basic_file, "w", "utf-8")


def is_all_chinese(ustr):
    for uchar in ustr:
        if not is_chinese(uchar):
            return False

    return True


def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    return False

num = 0
with codecs.open(ansj_dict_default_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print num

        array = line.strip().split("\t")

        word, nature, freq = array[0], array[1], array[2]
        if word not in wordDic:
            wordDic[word] = line.strip()

print "ansj dict num is ", num

ansjCoreFreq = 0
exportNum = 0
with codecs.open(ansj_dict_core_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split("\t")
        if len(array) != 6:
            continue
        natureInfo = array[5]
        if natureInfo == "null":
            continue

        word = array[1]

        natureList = list()
        freqList = list()

        natureInfo = array[5][1:-1]
        natureArray = natureInfo.split(",")
        for natureTerm in natureArray:
            index = natureTerm.index("=")
            nature = natureTerm[:index]
            freq = natureTerm[index+1:]

            natureList.append(nature)
            freqList.append(freq)

        ansj_basic_word.write(word+"\t"+','.join(natureList)+"\t"+','.join(freqList)+"\n")

        if word in wordDic:
            continue

        wordDic[word] = word+"\t"+','.join(natureList)+"\t"+','.join(freqList)

print 'ansj core.dic freq num is ', ansjCoreFreq
print 'ansj core.dic export num is ', exportNum

num = 0
extend_word = 0
with codecs.open(hanlp_dict_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print num

        array = line.strip().split("\t")
        word = array[0]

        if word == u"始##始" or word == u"末##末":
            continue

        if word in wordDic:
            continue

        freqList = list()
        natureList = list()

        max_freq = 0

        for i in range(1, len(array), 2):
            nature = array[i]
            freq = array[i+1]

            if max_freq < int(freq):
                max_freq = int(freq)

            freqList.append(freq)
            natureList.append(nature)

            extend_word += 1

        if is_all_chinese(word):
            wordDic[word] = word+"\t"+','.join(natureList)+"\t"+','.join(freqList)
            hanlp_extend_word.write(line)

print 'hanlp dict num is ', num
print 'hanlp extend word number is ', extend_word


# 与ansj字典相比额外补充34071个词，
# 但是词质量较一般（都是人名可以忽略）可以放弃,只补充英文开头的单词。
num = 0
exportNum = 0
with codecs.open(jieba_dict_file, "r", "utf-8") as f:
    for line in f:
        array = line.strip().split(" ")

        word = array[0]
        freq = array[1]
        nature = array[2]

        num += 1
        if num % 100000 == 0:
            print num

        if word not in wordDic and not is_chinese(word[:1]):
            wordDic[word.upper()] = word.upper()+"\t"+nature+"\t"+freq
            wordDic[word.lower()] = word.lower()+"\t"+nature+"\t"+freq
        else:
            exportNum += 1
            ansj_exetnd_word.write(line)

ansj_exetnd_word.close()

print 'jieba dict num is ', num
print 'jieba export num is ', exportNum
print 'merge dict num is ', len(wordDic)


outfile = codecs.open(merge_dict_file, "w", "utf-8")
for word in wordDic:
    outfile.write(str(wordDic[word])+"\n")
outfile.close()
