#!/usr/bin/python
#coding=utf-8  
import urllib
import simplejson as json
from HTMLParser import HTMLParser

import kuaisoo
import string
import time

current_session="ff"
def isAsciiChar(c):
    ascii_cnt=ord(c)
    if ascii_cnt >=0 and ascii_cnt <128:
        return True
    else:
        return False 

def strip_tags(html):

    html=html.strip()
    html=html.strip("\n")
    result=[]
    parse=HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

#def is_cmd(string):
def google_text(search_key_word,start=0):
    #query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'large',})

    #url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'% (query)
    #kuaisoo.log.info("url:%s"%url)
    query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'small','start':start})

    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s '% (query)
    kuaisoo.log.info(' fire url :%s'%url)
    search_results = urllib.urlopen(url)
        
        
    content=search_results.read()
    
    search_results.close()
    data = json.JSONDecoder().decode(content) 
    lst_result= data['responseData']['results']
    
    #dic_title_url={}
    result=""
    for res in lst_result:
        #dic_title_url[res['titleNoFormatting']]=res['url']
        #kuaisoo.log.info(str(res))
        content=res['content']
        content=strip_tags(content)
        result=result+"[%s]"%str(start+1)+res['titleNoFormatting']+":\r\n"+content+"\r\n"+res['url']+"\r\n"*2
        start = start +1
    return result

def get_next(wxPost):
    global current_session

    start =  current_session['start']
    start =start +4
    current_session['start']=start
    key_word= current_session['key_word']
    result=google_text(key_word,start=start)
    return result

def google_images(wxPost,start=0):
    return u"这会咱还不支持图片搜索哈"
    search_key_word="df"
    query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'small','start':start})
    #url = http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=Google&start=32
    url=''

def get_previous(wxPost):
    global current_session

    start =  current_session['start']
    start =start -4
    if start <0:
        start =0
    current_session['start']=start
    key_word= current_session['key_word']
    result=google_text(key_word,start=start)
    return result

def get_help(wxPost):
    return u"""
[n]ext:        下一页
[p]revious:    前一页
[h]elp:        帮助
[i]mages:        搜索图片
[a]bout:       关于
"""

text_response_tpl="""<xml>
 <ToUserName><![CDATA[%s]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName>
 <CreateTime>%s</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[%s]]></Content>
 </xml>"""
def get_about(wxPost):
    return u"通过微信上google!\r\n飞哥出品，必属精品！"

def unknown_cmd():
    #just a mark
    pass

#def google_text():
#    return None

wenhao_cn=u'\uff1f' # for android wei xin
google_action={'n':get_next,'i':google_images,'p':get_previous,'a':get_about,'h':get_help,'?':get_help,wenhao_cn:get_help,}
default_url='http://ajax.googleapis.com/ajax/services/search/web'

def is_cmd(key_word):
    global curent_session
    result=False
    length=len(key_word)
    try:
        kuaisoo.log.debug('key_word:%s'%key_word)

    except:
        kuaisoo.log.exception('you known')
        
    if length == 1:
        is_ascii = isAsciiChar(key_word)
        kuaisoo.log.debug("is_ascii:%s"%str(is_ascii))
        if is_ascii:
            #into cmd mode
            key_word=key_word.lower()
            kuaisoo.log.debug('key_word now:%s'%key_word)
            action=google_action.get(key_word,None)
            kuaisoo.log.debug('action now:%s'%str(action))
            
            if action is None:
                current_session['key_word']=key_word
                result= False
            else:
                result= True
        else:
            
            try:
                kuaisoo.log.debug("repr:%s"%repr(key_word))
                kuaisoo.log.debug("repr wenhao_cn:%s"%repr(wenhao_cn))
            except:
                pass
            if key_word == wenhao_cn:
                result = True

    else:
        result = False
    kuaisoo.log.debug("%s is cmd : %s"%(key_word,result))
    return result
            


def init(wxPost):
    global current_session
    #current_session = kuaisoo.Session.load_session(wxPost.FromUserName)
    current_session = kuaisoo.Session.load_session()
    kuaisoo.log.debug('current session:%s'%str(current_session))
    url= None
    start = 0
    #global current_session
    try:
        url= current_session['url']
    except:
        #session['url']=default_url
        
        #current_session.add('url',default_url) #['url']=default_url
        current_session['url']=default_url
        url = default_url
        
    
    try:
        start=  current_session['start']
    except:
         current_session['start']=0 

"""
def mk_query(search_key_word,start):
    query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'small',})
"""
def get_current_session():
    return current_session

def search_text(wxPost):
    
        
    try:
        init(wxPost)
        #current_session=get_current_session()
        global current_session

        kuaisoo.log.debug("session:%s"%str( current_session))
        
        content=wxPost.getNodeValue('Content')
        content = string.strip(content, ' ')
        kuaisoo.log.info("user input:%s"%content)
        if is_cmd(content):
            content=content.lower()
            action = google_action.get(content,None)

            response=action(wxPost)
        else:
            current_session['key_word']=content
            current_session['start']=0
            response = google_text(content)
        
        result = text_response_tpl%(wxPost.FromUserName,wxPost.ToUserName,time.time(),response)
        current_session.save()
        return result
    except:
        kuaisoo.log.exception("exception on search text")
        
    