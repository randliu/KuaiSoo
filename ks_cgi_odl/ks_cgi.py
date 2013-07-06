#!/usr/bin/python
#coding=utf-8  
import os

class Request:
    dict={}
    
    def __init__(self):
        for k,v in os.environ.items():
            self.dict[k] = v
            
    def __getitem__(self,key):
        return self.dict[key]   
    
    def __setitem__(self,key,value):
        self.dict[key]=value

class Response:
    pass
