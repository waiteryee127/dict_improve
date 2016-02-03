#!/usr/bin/env python
# -*- coding: utf-8

__author__ = 'Administrator'


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
