#!/usr/bin/python
#coding=utf-8  
import logging,os
import sys  
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback
from os import environ

import ks_http

ks_http.head()

for key in environ.keys():
    print key
    print "<br>"
    
print "-----------<br><br>"
print " sys.stdout.encoding =%s"%(sys.stdout.encoding)
for name ,value in environ.items():
    print "%s:%s"%(name,value)
    print "<br>"
    
print "-----------<br><br>"

for param in os.environ.keys():
    print "<b>%20s</b>: %s<br>" % (param, os.environ[param])

print sys.getdefaultencoding()