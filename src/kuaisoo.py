#!/usr/bin/python
#coding=utf-8  
import os,sys
import codecs
import StringIO
import logging
import logging.handlers  

import xml.dom.minidom
import hashlib
import pickle
import datetime

Token = "kuaisoo"

LOG_FILE = './log/ks.log'  

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)     
handler.setFormatter(formatter)        
  
log = logging.getLogger('handler')      
log.addHandler(handler)             
log.setLevel(logging.INFO)
#log.setLevel(logging.DEBUG)

import msg_action
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
        
        
session_expired_span = 120 #second
#current_session=None
wx_post =""

class Session:
    """
    wxid=None
    request_time = None
    current_search_type = "text"    #image
    current_page    =   0
    wxid=None
    """
    #`isExpired = False
    #dict={"wxid":None,"request_time":None,"current_search_type":"text","current_page":0}
    current_session=None

    def __init__(self,username):
        #self.wxid = wxid
        self.dict={}
        self.dict['wxid']=username
        self.dict['request_time']=datetime.datetime.now()
        #self.dict['uri']=uri
    
    def isExpired(self):
        delta=datetime.timedelta(seconds=session_expired_span)
        now = datetime.datetime.now()
        expire_date = self['request_time']+delta
        if now > expire_date:
            return True
        else:
            return False
        
    def set_time(self,time):
        #self.request_time = time
        self.dict['request_time'] = time
    def save(self):
        if self.dict['wxid'] is None:
            raise Exception("gonna save an session without name!")
        if self.dict['request_time'] is None:
            raise Exception("session request time not set!")
        
        self['request_time'] = datetime.datetime.now()
        file_name =  './session/%s'%self.dict['wxid']
        log.debug('session file name :%s '%file_name)
        f = open(file_name,'w')
        pickle.dump(self, f)
        f.close()
        
    @staticmethod
    def load_session():
        session = None
        user_name = None
        try:
            user_name = os.environ['FromUserName']
        except:
            pass
            
        if user_name is None:
            raise Exception("gonna load an session without NULL req!")
        f=None
        try:
            f = open('./session/%s'%user_name,'r')
            session = pickle.load(f)
            log.info("session[wxid]=%s"%session['wxid'])
            f.close()

        except:
            #a new user
            log.info("new user with wx id:%s"%user_name)
            session = Session(user_name)
        global current_session
        log.info('load session %s'%str(session))
        current_session=session
        log.info('current_session %s'%str(current_session))
        return session
    
    def __getitem__(self,key):
        return self.dict[key]   
    
    def __setitem__(self,key,value):
        self.dict[key]=value

class WXPost(ksObj):
    wx_xml=None
    
    """
    text_handler = None
    images_handler=None    
    location_handler=None
    """
    #action=None
    ToUserName=None
    FromUserName=None
    MsgType = None
    doc = None
    def getNodeValue(self,name):                     
        node = self.doc.getElementsByTagName(name)[0]
        value = node.childNodes[0].nodeValue
        return value
    def __init__(self,wx_xml):
        try:
            self.wx_xml=wx_xml
            self.doc = xml.dom.minidom.parseString(wx_xml)              
            self.ToUserName=self.getNodeValue('ToUserName')
            self.FromUserName=self.getNodeValue('FromUserName')
            self.MsgType=self.getNodeValue('MsgType')
        except:
            log.exception("exception in WXPost().__init__()  ")
    
    def unknownMsgType(self):
        return "未知的消息类型.\r\n msg body:%s"%self.wx_xml
    """  
    def set_action(self,action):
        self.action = action
        pass
    """  
    def handle(self):
        
        handlers={'text':msg_action.text_handler,'image':msg_action.images_handler,'location':msg_action.location_handler}
        
        #将消息分发到对应的处理方法
        action = handlers.get(self.MsgType,self.unknownMsgType())
        log.debug('action :%s'%repr(action))
        #return action(self)
        result=''
        try:
            
            result = action(self)
            if not isinstance(result,basestring):
                raise Exception("user action returns not string, but %s"%(str(result)))
        except:
            log.exception("exception on handle msg")
        return result

        
        
class Request(ksObj):    
    wxPost=None
    def __init__(self):
        for param in os.environ.keys():
            self.dict[param]=  os.environ[param]
        if self.dict['REQUEST_METHOD']=='POST':
            try:
                wx_post_xml=sys.stdin.read()
                self.wxPost=WXPost(wx_post_xml)
                log.debug(wx_post_xml)
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
    
    def get_content(self):
        return self.output.getvalue()
        
if __name__ == '__main__':
    #os.environ['QUERY_STRING'] ='signature=aa65a477e879c65dbc27d3209e92be7d362082de&echostr=5825623491949821499&timestamp=1356267067&nonce=1356383665'
    #os.environ['QUERY_STRING']='signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928&echostr=tfffff'
    #os.environ['REQUEST_URI']='/scgi-bin/handler.py?signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928'
    #os.environ['REQUEST_METHOD']='GET'
    #print os.environ['REQUEST_METHOD']
    #sys.exit()
    log.info("\r\n----------------start---------------------\r\n")
    req= Request()

    if req['REQUEST_METHOD'] == 'GET':
        t=valid(req)
        response= Response(t)
        response.purge()
        sys.exit()
        
    # now handling request
    
    try:
        p = req.wxPost

        p.text_handler = msg_action.text_handler
        p.images_handler = msg_action.images_handler
        p.location_handler = msg_action.location_handler
        os.environ['FromUserName'] = p.FromUserName
        #session = Session.load_session(p.FromUserName)
        #log.info('current session:%s'%str(current_session))
        result = p.handle()
        response = Response(result)
        content=response.get_content()
        log.info("return %s"%content)
        #log.info("session expired :%s"%str(session.isExpired()))
        response.purge()

        #session.save()
        
    except:
        log.exception("kuaisoo exception")
    log.info("\r\n----------------end---------------------\r\n\r\n")


    

    

