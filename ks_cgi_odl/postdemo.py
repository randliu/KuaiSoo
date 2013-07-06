#!/usr/bin/python
#coding=utf-8  
import logging,os
import sys  
import traceback
from os import environ

import ks_http


ks_http.head()

import cgi
form = cgi.FieldStorage()
print str(form)
print form["firstName"]