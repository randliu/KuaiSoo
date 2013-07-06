#!/usr/bin/python
#coding=utf-8  
import pickle
import datetime

"""
需要在session中记录的内容：
1. 用户id，用微信号
2. 上次请求的时间
3. 当前的状态：
    a.    text or img 
    b.    当前第几页  start = or label = ,可能用label = 好些
    

"""
expired_span = 120 #second

class Session:
    """
    wxid=None
    request_time = None
    current_search_type = "text"    #image
    current_page    =   0
    wxid=None
    """
    #`isExpired = False
    dict={"wxid":None,"request_time":None,"current_search_type":"text","current_page":0}
    def __init__(self,wxid,uri):
        #self.wxid = wxid
        self.dict['wxid']=wxid
        self.dict['request_time']=datetime.datetime.now()
        self.dict['uri']=uri
        
    def isExpired(self):
        delta=datetime.timedelta(seconds=expired_span)
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
        
        f = open(self.dict['wxid'],'w')
        pickle.dump(self, f)
        f.close()
        
    @staticmethod
    def load_session(wxid):
        if wxid is None:
            raise Exception("gonna load an session without name!")
        f = open(wxid,'r')
        session = pickle.load(f)
        return session
    
    def __getitem__(self,key):
        return self.dict[key]   
    
    def __setitem__(self,key,value):
        self.dict[key]=value
        
        
        