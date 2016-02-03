#!/usr/bin/env python
# -*- coding: utf-8

__author__ = 'Administrator'
import codecs
import urllib2

dicta = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "BAIDUID=5FB4E2A59C363647D3FDF46B2C3E306A:FG=1; "
              "BIDUPSID=5FB4E2A59C363647D3FDF46B2C3E306A; "
              "PSTM=1436160872; BDUSS=TNIVGdYSHVlb2o2V1EwZ2IwOHRhVjJVYmhFNm1STDBuR0N2d2xwSXVzWkFJOWx"
              "WQVFBQUFBJCQAAAAAAAAAAAEAAAAO7PkOd2FpdGVyeWVlMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
              "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAECWsVVAlrFVY; ispeed=1; MCITY=-%3A; BDSFRCVID=XVksJeCCxG34Pfv4_"
              "iqZo44UhDweuWgL9Fsp3J; H_BDCLCKID_SF=JRAjoK-XJDv8fJ6xq4vhh4oHjHAX5-RLfabpB-OF5lOTJh0Rjh3"
              "t560mMqQz250JQCbRLb5aQb3dbqQRK5bke4tX-NFtqTDDJU5; ispeed_lsm=2; BD_HOME=1; "
              "BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; H_PS_PSSID=1424_18155_17947_17971_17833_17001_"
              "17073_15016_12156_10632; B64_BOT=1; BD_UPN=12314353; H_PS_645EC=5611hJbWK2KmUclg5BTgFIE9iN"
              "%2Bbf%2F735MIq2uPpYqWjfEbgsuzKSSrG5dQ",
    "Host": "www.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36"
}

ROOT_SPIDER_PATH = "../data/spiderdata/"

output_word_baidu_file = ROOT_SPIDER_PATH+"word.filterbaidu"
output_baidu = codecs.open(output_word_baidu_file, "w", "utf-8")
output_word_file = ROOT_SPIDER_PATH+"word.alternative"


def get_info_by_baidu(word_alter):
    request = urllib2.Request("https://www.baidu.com/s?wd="+word_alter)
    for key in dicta:
        request.add_header(key, dicta[key])

    response = urllib2.urlopen(request)
    home_html = response.read()

    try:
        if u"仍然搜索：" in home_html:
            return "error"
        if word_alter+u"</em>_百度图片" in home_html \
                or word_alter+u"</em>_互动百科" in home_html \
                or word_alter+u"</em>_百度百科" in home_html \
                or u"京东" in home_html or u"天猫" in home_html \
                or u"当当" in home_html:
                return "word"

        return "none"
    except Exception as e:
        print e
        return "error"

num = 0
with codecs.open(output_word_file, "r", "utf-8") as f:
    for line in f:
        num += 1
        if num % 100 == 0:
            print "scrapy number is ", num
        info = get_info_by_baidu(line.strip())
        output_baidu.write(info+":"+line.strip()+"\n")
output_baidu.close()
