#!/usr/bin/python
#coding=utf-8  

help_info = u"""
快捷命令
[n]ext          下一页
[p]revious      上一页
[i]mage         图片搜索
[a]bout         kuaisoo
?               查看快搜命令
----------------
快搜真心为您！
"""

import sys
import codecs
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
print >>sys.stdout,"test"
print >>sys.stdout, help_info