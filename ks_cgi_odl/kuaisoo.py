#!/usr/bin/python
#coding=utf-8  
import os,sys
import codecs
import StringIO
import logging
import logging.handlers  

import xml.dom.minidom
import hashlib
import user_action

Token = "kuaisoo"

LOG_FILE = './log/ks.log'  

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)     
handler.setFormatter(formatter)        
  
log = logging.getLogger('handler')      
log.addHandler(handler)             
log.setLevel(logging.INFO)

def get_url_args(query_string):
    query_dict={}
    lst_k_v = query_string.split('&')
    for k_v in lst_k_v:
        tmp=k_v.split('=')
        query_dict[tmp[0]]=tmp[1]
        
    return query_dict


def valid(req):
    QUERY_STRING=req['QUERY_STRING']
    log.info('QUERY_STRING:%s'%QUERY_STRING)
    args=get_url_args(QUERY_STRING)
    arr=[Token, args['timestamp'],args['nonce']]
    #print arr
    s_arr=sorted(arr)
    tmpstr=''.join(s_arr)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    #log.info("tmpstr:%s"%tmpstr)
    if tmpstr == args['signature'] :
        return  args['echostr']
    else:
        return None

class ksObj(object):
    dict={}
    def __getitem__(self,key):
        return self.dict[key]
    def __init__(self):
        self.lst={}
    def add(self,k,v):
        self.lst[k]=v
    def __setitem__(self,key,value):
        self.dict[key]=value
        
        
def getValue(doc,val):                     
    node = doc.getElementsByTagName(val)[0]
    value = node.childNodes[0].nodeValue
    return value

class WXPost(ksObj):
    wx_xml=None
    
    
    text_handler = None
    images_handler=None    
    location_handler=None

    def __init__(self,wx_xml):
        try:
            self.wx_xml=wx_xml
            doc = xml.dom.minidom.parseString(wx_xml)              
            self.ToUserName=getValue(doc,'ToUserName')
            self.FromUserName=getValue(doc,'FromUserName')
            self.MsgType=getValue(doc,'MsgType')
        except:
            log.exception("exception in WXPost().__init__()  ")
    
    def unknownMsgType(self):
        pass    
    def handle(self):
        handlers={'text':self.text_handler,'images':self.images_handler,'location':self.location_handler}
        
        

        
        
class Request(ksObj):    
    wxPost=None
    def __init__(self):
        for param in os.environ.keys():
            self.dict[param]=  os.environ[param]
        if self.dict['REQUEST_METHOD']=='POST':
            try:
                wx_post_xml=sys.stdin.read()
                self.wxPost=WXPost(wx_post_xml)
            except:
                log.exception("exception in Request.__init__() when found its a post req")
                
 
class Response(ksObj):
    output = StringIO.StringIO()
    def __init__(self,content):
        print >> self.output, "Content-type:text/html\r\n"
        print >> self.output,content
        
    def purge(self):
        if sys.stdout.encoding != 'UTF-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
        print >> sys.stdout,self.output.getvalue()
        
if __name__ == '__main__':
    #os.environ['QUERY_STRING'] ='signature=aa65a477e879c65dbc27d3209e92be7d362082de&echostr=5825623491949821499&timestamp=1356267067&nonce=1356383665'
    #os.environ['QUERY_STRING']='signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928&echostr=tfffff'
    #os.environ['REQUEST_URI']='/scgi-bin/handler.py?signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928'
    #os.environ['REQUEST_METHOD']='GET'
    #print os.environ['REQUEST_METHOD']
    #sys.exit()
    req= Request()

    if req['REQUEST_METHOD'] == 'GET':
        t=valid(req)
        response= Response(t)
        response.purge()
        sys.exit()
        
    # now handling request
    p = req.wxPost
    p.text_handler = MsgHandlerConfig.handlers['text']
    p.images_handler = MsgHandlerConfig.handlers['images']
    p.location_handler = MsgHandlerConfig.handlers['location']
    result = p.wxPost.handle()
    response = Response(result)
    response.purge()
    

    

