#!/usr/bin/python
#coding=utf-8  
import sys
import codecs

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
    
import logging
import logging.handlers  
import urllib2, urllib    
import simplejson as json
from HTMLParser import HTMLParser


fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s' 

LOG_FILE = './log/ks.log'  

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)     
handler.setFormatter(formatter)        
  
log = logging.getLogger('handler')      
log.addHandler(handler)             
log.setLevel(logging.INFO)  

def head():
    print "Content-type:text/html\r\n"

def strip_tags(html):

    html=html.strip()
    html=html.strip("\n")
    result=[]
    parse=HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    return "".join(result)
    
def google(search_key_word):
    query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'large',})

    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'% (query)
    log.info("url:%s"%url)
    query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'small',})

    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s '% (query)
    search_results = urllib.urlopen(url)
        
        
    content=search_results.read()
    
    search_results.close()
    data = json.JSONDecoder().decode(content) 
    lst_result= data['responseData']['results']
    
    #dic_title_url={}
    result=""
    for res in lst_result:
        #dic_title_url[res['titleNoFormatting']]=res['url']
        #log.info(str(res))
        content=res['content']
        content=strip_tags(content)
        result=result+res['titleNoFormatting']+":\r\n"+content+"\r\n"+res['url']+"\r\n"*2
    return result
   
def isAsciiChar(c):
    ascii_cnt=ord(c)
    if ascii_cnt >=0 and ascii_cnt <128:
        return True
    else:
        return False 