#!/usr/bin/env python3
# coding: utf-8
from time import localtime, time, strftime

__author__ = 'Jux.Liu'


def log(*args, **kwargs):
    # time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    time_fromat = '%Y/%m/%d %H:%M:%S'
    value = localtime(int(time()))
    dt = strftime(time_fromat, value)
    print(dt, *args, **kwargs)
