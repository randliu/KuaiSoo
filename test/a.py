import pickle
import kuaisoo
import os

def buildRequestPost():
    os.environ['REQUEST_METHOD']='POST'
    fd = os.open("text_msg.txt", os.O_RDONLY)
    os.dup2(fd, 0)
    req= kuaisoo.Request()
    #print self.req.get_post_data()
    os.close(fd)
    return req
req= buildRequestPost()
sess=kuaisoo.Session(req)
print 1
print sess['wxid']
f=open('./session/oaEn2jhk1nCu9VREAmtTDufQd5kw','r')
o=pickle.load(f)
print 2
print o['wxid']
f.close()


