#!/usr/bin/python
#coding=utf-8  
#对不同类型的消息设置处理方法
#import kuaisoo.WXPost
from kuaisoo import log
import time
import string
import os
#from kuaisoo import Session

"""
def text_handler(wx_post):
    #wx_post: class kuaisoo.WXPost
    return "text"


def images_handler(wx_post):
    pass


def location_handler(wx_post):
    pass
"""
#-----------------------------------
text_tpl="""<xml>
 <ToUserName><![CDATA[%s]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName>
 <CreateTime>%s</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 </xml>"""
import google_wx
import string

def on_guanzhu():
    result = u"""微信上的快速搜索\r\n
[N]ext:        下一页
[P]revious:    前一页
[I]mages:      搜索图片
[A]bout:       关于
?:             帮助
"""
    return result
text_response_tpl="""<xml>
 <ToUserName><![CDATA[%s]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName>
 <CreateTime>%s</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 </xml>"""
 
def text_handler(wx_post):
    #log.info('result:%s'%(str))
    """
    sess = Session.load_session(wx_post.FromUserName)
    
    content = google.search(wx_post.getNodeValue('Content'))
    
    result = text_tpl%(wx_post.FromUserName,wx_post.ToUserName,time.time(),content)
    return result
    """
    key='Hello2BizUser'
    result=None
    if wx_post:
        content=wx_post.getNodeValue('Content')
        content = string.strip(content, ' ')
        if content == key:
            #this is a 关注 msg
            log.info("new GuanZhu:%s"%os.environ['FromUserName'])
            result=on_guanzhu()
            result = text_response_tpl%(wx_post.FromUserName,wx_post.ToUserName,time.time(),result)
        
        else:
            result = google_wx.search_text(wx_post)
    return result

def images_handler(wx_post):
    result = text_response_tpl%(wx_post.FromUserName,wx_post.ToUserName,time.time(),u"伦家不认识图片哦～")
    return result
   



def location_handler(wx_post):
    result = text_response_tpl%(wx_post.FromUserName,wx_post.ToUserName,time.time(),u"坏淫～")
    return result
    return wx_post.wx_xml
