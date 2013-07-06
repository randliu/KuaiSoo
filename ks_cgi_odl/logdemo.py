#!/usr/bin/python
#coding=utf-8  
import logging,os
import sys  
import traceback

import ks_http

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG)  
log = logging.getLogger('root.test')  
log.setLevel(logging.WARN)  

ks_http.head()
try: 

    print "OK2"
    # blank line, end of headers

    print "<html><header><title>LogDemo</title></header><body>Hello CGI!</body></html>"

    log.info('info')   
    log.debug('debug')  
    log.warning('warnning')  
    log.error('error')  

    print "OK3"
except: 
    traceback.print_exc(file=sys.stdout)