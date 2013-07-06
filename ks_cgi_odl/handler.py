#!/usr/bin/python
#coding=utf-8  
# Import modules for CGI handling 
import cgi, cgitb 
import hashlib
import logging
import os,sys

import simplejson as json
import traceback
import xml.dom.minidom  
import time
cgitb.enable()
import string

import ks_http
from ks_http import log

import cmd
Token = "kuaisoo"

log.info("------------start--------------------\r\n")
"""
os.environ['REQUEST_METHOD']='GET'
os.environ['QUERY_STRING']='signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928&echostr=tfffff'
os.environ['REQUEST_URI']='/scgi-bin/handler.py?signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928'
"""

REQUEST_METHOD = os.environ['REQUEST_METHOD']
REQUEST_URI= os.environ['REQUEST_URI']
QUERY_STRING = os.environ['QUERY_STRING']
log.info ("%s on %s"%(REQUEST_METHOD,REQUEST_URI))

ks_http.head()


def getValue(doc,val):                     
    node = doc.getElementsByTagName(val)[0]
    value = node.childNodes[0].nodeValue
    return value


def on_cmd(command):
    log.info("enter command mode with command :%s"%str(command))
    #return (cmd_result,isValidCmd)
    #isvalidCmd=False
    if command == '?':
        return (cmd.help_info,True)
    else:
        return (None,False)
        

    
def on_text_msg(doc):
    Content=getValue(doc,'Content')
    Content = string.strip(Content,' ')
    length = len(Content)
    length_info="request content length:%s"%str(length)
    log.info(length_info)
    if length == 1:
        is_ascii = ks_http.isAsciiChar(Content)
        if is_ascii:
            #into cmd mode
            (cmdResult,isValidCmd)= on_cmd(Content)
            if isValidCmd:
                return cmdResult
            else:
                #invalid cmd, so go on google
                pass
    Content=ks_http.google(Content)
    return Content

def on_image_msg(doc):
    return u"亲，不认识图片呢"
    
def on_location_msg(doc):
    return u"亲，地理位置未来将支持！"
    
text_tpl="""<xml>
 <ToUserName><![CDATA[%s]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName>
 <CreateTime>%s</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 </xml>"""
 
image_tpl="""<xml>
                            <ToUserName><![CDATA[%s]]></ToUserName>
                            <FromUserName><![CDATA[%s]]></FromUserName>
                            <CreateTime>%s</CreateTime>
                            <MsgType><![CDATA[%s]]></MsgType>
                            <Content><![CDATA[%s]]></Content>
                            <FuncFlag>0</FuncFlag>
                            </xml>"""
                            
msg_handler={"location":on_location_msg,"text":on_text_msg,"image":on_image_msg}

def unknown_msg_type(msg_type):
    log.error("unknown msg type %s"%str(msg_type))
    
def on_post():
    raw_post=sys.stdin.read() 
    log.info("raw:%s"%str(raw_post))
    doc = xml.dom.minidom.parseString(raw_post)  
    
    try:
        
        ToUserName=getValue(doc,'ToUserName')
        FromUserName=getValue(doc,'FromUserName')
        MsgType=getValue(doc,'MsgType')
        #location image text
        handler=msg_handler.get(MsgType,unknown_msg_type)
        content=handler(doc)
        """
        CreateTime=getValue(doc,'CreateTime')
        MsgType=getValue(doc,'MsgType')
        Content=getValue(doc,'Content')
        Content=ks_http.google(Content)
        """
        #Content=getValue(doc,'Label')
        #print Content
        #log.info(Content)
        response = """<xml>
 <ToUserName><![CDATA[%s]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName>
 <CreateTime>%s</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 </xml>"""%(FromUserName,ToUserName,time.time(),content)
 
                
        log.info("response:%s"%response)

        print response
    except:
        log.exception("exception in on_post")
    return 

def get_url_args(query_string):
    query_dict={}
    lst_k_v = query_string.split('&')
    for k_v in lst_k_v:
        tmp=k_v.split('=')
        query_dict[tmp[0]]=tmp[1]
        
    return query_dict

def valid():
    args=get_url_args(QUERY_STRING)
    print args['echostr']
    
action={"POST":on_post,"GET":valid}


def faultREQUEST_METHOD():
    log.error("unknown REQUEST_METHOD :%s"%REQUEST_METHOD)
    
action.get(REQUEST_METHOD,faultREQUEST_METHOD)()

for param in os.environ.keys():
    log.info( "<b>%20s</b>: %s<br>" % (param, os.environ[param]))
log.info("------------end--------------------\r\n\r\n")



