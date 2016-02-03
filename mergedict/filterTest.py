#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
wordDic = {}
wordCiXingDic = {}
danziDic = {}
outfile = codecs.open("parseMerge.dic","w","utf-8")

num = 0

with codecs.open("../data/originaldata/merge.dic", "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print num

        array = line.strip().split("\t")
        if len(array) != 3:
            continue

        wordCiXingDic[array[0]] = array[1]
        arrayCixing = array[1].split(",")
        for arrayTerm in arrayCixing:
            if arrayTerm  in ['n','v','nz','vi','vn']:
                break
        else:
            continue

        if array[0] not in wordDic:
            wordDic[array[0]] = []

num = 0
with codecs.open("../data/originaldata/merge.dic","r","utf-8") as f:
    for line in f:
        num += 1
        if num % 100000 == 0:
            print num
        array = line.strip().split("\t")
        if len(array) != 3:
            continue

        word_len = len(array[0])
        if word_len < 3:
            continue

        arrayCixing = array[1].split(',')
        for arrayTerm in arrayCixing:
            if arrayTerm in ['nz','n']:
                break
        else:
            continue
        if array[0] == u"牛肉馅":
            print line
        for i in range(2,len(array[0])):
            if array[0][:i] in wordDic:
                wordDic[array[0][:i]].append(array[0]+"|"+array[1])


for line in wordDic:
    if len(wordDic[line]) == 0:
        continue
    for wordInfo in wordDic[line]:
        array = wordInfo.split("|")
        wordBig = array[0]
        cixingBig = array[1]
        wordOne = line
        cixingOne = wordCiXingDic[wordOne]
        wordTwo = wordBig[len(wordOne):]
        if wordTwo not in wordCiXingDic:
            continue
        cixingTwo = wordCiXingDic[wordTwo]
        if wordBig == u'牛肉馅':
            print wordOne,cixingOne,wordTwo,cixingTwo
        if cixingBig == "n":
            cixingOneArray = cixingOne.split(",")
            cixingTwoArray = cixingTwo.split(",")
            for term in cixingOneArray:
                if term in ['vi','vn','n']:
                    break
            else:
                for term2 in cixingTwoArray:
                    if term2 in ['vi','vn','n']:
                        break
                else:
                    continue

            if cixingOne == 'n' and cixingTwo == 'n':
                continue
        
        if cixingTwo in ['n','nz','ag']:
            outfile.write(wordBig+"\t")
            outfile.write(wordOne+"\t")
            outfile.write(cixingOne+"\t")
            outfile.write(wordTwo+"\t")
            outfile.write(cixingTwo)
            outfile.write("\n")
        

outfile.close()
#first is n  last is nz
#first is v  last is nz
#first is nz last is nz
#remind is n or nz  
