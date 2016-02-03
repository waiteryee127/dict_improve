#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaobin'
'''
把merge后的词典进行过滤，比如将一些姓名，机构名等词作为专有名词提取出
'''

import codecs

ROOT_FILTER_PATH = "../data/filterdata/"
ROOT_ORIGINAL_PATH = "../data/originaldata/"
ROOT_SPIDER_PATH = "../data/spiderdata/"

input_file = ROOT_ORIGINAL_PATH+"merge.dic"
output_file = ROOT_FILTER_PATH+"merge.dic"


china_name_file = ROOT_FILTER_PATH+"china_name.dic"
china_name_output = codecs.open(china_name_file, "w", "utf-8")

foreign_name_file = ROOT_FILTER_PATH+"foreign_name.dic"
foreign_name_output = codecs.open(foreign_name_file, "w", "utf-8")

org_name_file = ROOT_FILTER_PATH+"org_name.dic"
org_name_output = codecs.open(org_name_file, "w", "utf-8")

company_name_file = ROOT_FILTER_PATH+"company_name.dic"
company_name_output = codecs.open(company_name_file, "w", "utf-8")

republic_name_file = ROOT_FILTER_PATH+"republic_name.dic"
republic_name_output = codecs.open(republic_name_file, "w", "utf-8")

hospital_name_file = ROOT_FILTER_PATH+"hospital_name.dic"
hospital_name_output = codecs.open(hospital_name_file, "w", "utf-8")

college_name_file = ROOT_FILTER_PATH+"college_name.dic"
college_name_output = codecs.open(college_name_file, "w", "utf-8")

combine_name_file = ROOT_FILTER_PATH+"combine.dic"
combine_name_output = codecs.open(combine_name_file, "w", "utf-8")

brand_name_file = ROOT_SPIDER_PATH+"brand.firsthand"


brand_dict = dict()
with codecs.open(brand_name_file, "r", "utf-8") as f:
    for line in f:
        brand_dict[line.strip()] = 1


wordDic = {}
wordNatureDic = {}
wordFreqDic = {}
singleDic = {}
splitFreq = 10
num = 0

with codecs.open(input_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 10000 == 0:
            print "read number is ", num

        array = line.strip().split("\t")
        if len(array) != 3:
            continue

        word, nature, freq = array[0], array[1], array[2]

        wordNatureDic[word] = nature
        wordFreqDic[word] = freq
        arrayNature = nature.split(",")
        """
        if word not in wordDic:
            wordDic[word] = 1
        """
        for natureTerm in arrayNature:
            if natureTerm in ['n', 'v', 'nz', 'vi', 'vn'] and array[0] not in wordDic:
                wordDic[word] = 1


def get_china_name(word_china, nature_china, freq_china):
    """
    过滤词频较低较差的人名词
    :param word_china:
    :param nature_china:
    :param freq_china:
    :return:
    """
    if 'nr' != nature_china:
        return False

    if int(freq_china) > 29:
        return False

    line_china = word_china+"\t"+nature_china+"\t"+freq_china+"\n"
    china_name_output.write(line_china)
    return True


def get_foreign_name(word_foreign, nature_foreign, freq_foreign):
    """
    mergeDic中保留小于8个字的nrf词性数据
    :param word_foreign: 词语，欧美人名
    :param nature_foreign: 词性
    :param freq_foreign:  词频
    :return: boolean
    """
    if 'nrf' != nature_foreign:
        return False

    if len(word_foreign) < 8:
        return False

    line_foreign = word_foreign+"\t"+nature_foreign+"\t"+freq_foreign+"\n"
    foreign_name_output.write(line_foreign)
    return True


def get_org_name(word_org, nature_org, freq_org):
    """
    mergeDic保留小于4个字的机构名称
    :param word_org: 词语，组织机构名
    :param nature_org: 词性
    :param freq_org: 词频
    :return: boolean
    """
    if 'nt' != nature_org:
        return False

    if len(word_org) < 4:
        return False

    line_org = word_org+"\t"+nature_org+"\t"+freq_org+"\n"
    org_name_output.write(line_org)
    return True


def get_republic_name(word_republic, nature_republic, freq_republic):
    """
    政府机构词典
    :param word_republic: 词语，政府机构
    :param nature_republic: 词性
    :param freq_republic: 词频
    :return: boolean
    """
    if 'nto' != nature_republic:
        return False

    line_republic = word_republic+"\t"+nature_republic+"\t"+freq_republic+"\n"
    republic_name_output.write(line_republic)
    return True


def get_company_name(word_comp, nature_comp, freq_comp):
    """
    mergeDic保留小于4个字的公司
    :param word_comp: 词语，公司名
    :param nature_comp: 词性
    :param freq_comp: 词频
    :return: boolean
    """
    if 'ntc' != nature_comp:
        return False

    if len(word_comp) < 4:
        return False

    line_comp = word_comp+"\t"+nature_comp+"\t"+freq_comp+"\n"
    company_name_output.write(line_comp)
    return True


def get_hospital_name(word_hosp, nature_hosp, freq_hosp):
    """
    医院词典
    :param word_hosp: 词语
    :param nature_hosp: 词性
    :param freq_hosp: 词频
    :return: boolean
    """
    if 'nth' != nature_hosp:
        return False

    line_hosp = word_hosp+"\t"+nature_hosp+"\t"+freq_hosp+"\n"
    hospital_name_output.write(line_hosp)
    return True


def get_college_name(word_coll, nature_coll, freq_coll):
    """
    mergeDic保留小于6个字的大学
    :param word_coll: 词语，大学
    :param nature_coll: 词性
    :param freq_coll: 词频
    :return: boolean
    """

    if 'ntu' != nature_coll:
        return False

    if len(word) < 6:
        return False

    line_coll = word_coll+"\t"+nature_coll+"\t"+freq_coll+"\n"
    college_name_output.write(line_coll)
    return True


def remove_combine_word(word_cb, nature_cb, freq_cb):
    """
    明显的粗粒度不成词的词语踢去出词典
    :param word_cb: 词语
    :param nature_cb: 词性
    :param freq_cb: 词频
    :return: boolean
    """
    if ',' in freq_cb:
        return False
        # freq_cb = max(int(freq_cb[:freq_cb.index(',')]), int(freq_cb[freq_cb.rindex(',')+1:]))
    if len(word_cb) < 3 or int(freq_cb) >= splitFreq:
        return False

    if nature_cb not in ['nz', 'n', 'l', 'v', 'i', 'gm', 'gp', 'gc', 'gb', 'gg', 'gi']:
        return False

    is_remove = False
    for i in range(2, len(word_cb)):
        if word_cb[:i] in wordDic:
            is_remove = analysis_word(word_cb, word_cb[:i], nature_cb)
            if is_remove:
                line_cb = word_cb+"\t"+nature_cb+"\t"+freq_cb+"\n"
                combine_name_output.write(line_cb)
                return is_remove
    return is_remove


def analysis_word(word_big, word_one, nature_big):
    nature_one = wordNatureDic[word_one]
    freq_one = wordFreqDic[word_one]
    if ',' in freq_one:
        freq_one = max(int(freq_one[:freq_one.index(',')]), int(freq_one[freq_one.rindex(',')+1:]))
    word_two = word_big[len(word_one):]
    if word_two not in wordNatureDic:
        return False
    nature_two = wordNatureDic[word_two]
    freq_two = wordFreqDic[word_two]
    if ',' in freq_two:
        freq_two = max(int(freq_two[:freq_two.index(',')]), int(freq_two[freq_two.rindex(',')+1:]))

    if len(word_big) < 4:
        if nature_big == "nz":
            if int(freq_one) < splitFreq or int(freq_two) < splitFreq:
                return False

            if 'n' == nature_one and 'n' == nature_two:
                return False

            if nature_one in ['n', 'nz'] and nature_two in ['n', 'nz']:
                if word_one in brand_dict:
                    return True

        return False
    if nature_one == 'n' and nature_two == 'n':
        return False

    if nature_two in ['vi', 'd', 'an']:
        return False

    if int(freq_one) >= splitFreq*10 and int(freq_two) >= splitFreq*10:
        return True
    """
    if nature_big in ['n', 'nz']:

    if nature_big in ['l', 'v', 'i', 'gm', 'gp', 'gc', 'gb', 'gg', 'gi']:
        if int(freq_one) >= splitFreq*10 and int(freq_two) >= splitFreq*10:
            return True
        """
    return False

output = codecs.open(output_file, "w", "utf-8")
read_num = 0
leave_num = 0
with codecs.open(input_file, "r", "utf-8") as f:
    for line in f:
        read_num += 1
        if read_num % 10000 == 0:
            print "read number is ", read_num

        array = line.strip().split('\t')
        if len(array) != 3:
            continue

        word, nature, freq = array[0], array[1], array[2]

        '''
        # 直接剔除中文人名
        if 'nr' == nature:
            continue
        '''

        # 直接剔除工厂名
        if 'ntcf' == nature:
            continue

        # 剔除酒店名
        if 'ntch' == nature:
            continue

        # 剔除中小学
        if 'nts' == nature:
            continue

        if get_foreign_name(word, nature, freq) or get_org_name(word, nature, freq) \
                or get_company_name(word, nature, freq) or get_republic_name(word, nature, freq) \
                or get_hospital_name(word, nature, freq) or get_college_name(word, nature, freq) \
                or remove_combine_word(word, nature, freq) or get_china_name(word, nature, freq):
            continue

        output.write(line)
        leave_num += 1

foreign_name_output.close()
org_name_output.close()
company_name_output.close()
republic_name_output.close()
hospital_name_output.close()
college_name_output.close()
output.close()

print 'leave number is ', leave_num

