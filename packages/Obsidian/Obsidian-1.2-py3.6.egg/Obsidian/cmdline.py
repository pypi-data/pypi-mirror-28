#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# file name: cmdline.py
# description: TODO
# create date: 2016-09-19 14:43:48
# author: amoblin
# This file is created by Marboo<http://marboo.io> template file $MARBOO_HOME/.media/starts/default.py
# 本文件由 Marboo<http://marboo.io> 模板文件 $MARBOO_HOME/.media/starts/default.py 创建

import os
import sys
import scrapy.cmdline

base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))

def execute():
    if len(sys.argv) <= 1:
        print("usage: %s [config file]" % sys.argv[0])
        sys.exit(0)
    filename = sys.argv[1]

    output = os.path.join(os.getcwd(), "obsidian_output.json")
    if len(sys.argv) > 2:
        output = sys.argv[2]

    if not output.startswith('/'):
        output = os.path.join(os.getcwd(), output)

    if not filename.startswith('/'):
        filename = os.path.join(os.getcwd(), filename)

    if not os.path.isfile(filename):
        print("file not exist: %s" % sys.argv[1])
        sys.exit(0)

    os.chdir(os.path.join(base, "spiders"))
    scrapy.cmdline.execute(("scrapy runspider jsonspider.py -a path=%s -o %s" % (filename, output)).split())

if __name__ == "__main__":
    execute()
