import random
import os
import unittest


os.environ['QUERY_STRING']='signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928&echostr=tfffff'
os.environ['REQUEST_URI']='/scgi-bin/handler.py?signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928'
#os.environ['REQUEST_METHOD']='POST'

import kuaisoo

def buildRequestPost():
    os.environ['REQUEST_METHOD']='POST'
    fd = os.open("text_msg.txt", os.O_RDONLY)
    os.dup2(fd, 0)
    req= kuaisoo.Request()
    #print self.req.get_post_data()
    os.close(fd)
    return req

class TestRequstPOST(unittest.TestCase):
    req=None
    def setUp(self):
        self.seq = range(10)
        os.environ['REQUEST_METHOD']='POST'
        fd = os.open("text_msg.txt", os.O_RDONLY)
        os.dup2(fd, 0)
        self.req= kuaisoo.Request()
        #print self.req.get_post_data()
        os.close(fd)

    def test_action(self):
        data = self.req.wxPost.handle()
        print data 
        self.assertNotEqual(data, None, 'read post data')

class TestWXPost(unittest.TestCase):
    p=None
    def setUp(self):
        msg = """<xml><ToUserName><![CDATA[gh_1ff87fe87f88]]></ToUserName>
<FromUserName><![CDATA[oaEn2jhk1nCu9VREAmtTDufQd5kw]]></FromUserName>
<CreateTime>1356344005</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[u]]></Content>
</xml>"""
        self.p=kuaisoo.WXPost(msg)
    def test_ToUserName(self):
        self.assertEqual(self.p.ToUserName, 'gh_1ff87fe87f88')
    def test_FromUserName(self):
        self.assertEqual(self.p.FromUserName, 'oaEn2jhk1nCu9VREAmtTDufQd5kw')   
    def test_MsgType(self):
        self.assertEqual(self.p.MsgType, 'text')   
        
    def test_handle(self):
        result = self.p.handle()
        #print result
        #assert
class TestRequstGET(unittest.TestCase):
    req=None
    def setUp(self):
        
        os.environ['REQUEST_METHOD']='GET'
        self.req= kuaisoo.Request()
    

    def test_METOD(self):
        self.assertEqual(self.req['REQUEST_METHOD'], 'GET', 'GET METHOD')
        
class SessionTest(unittest.TestCase):
    sess=None
    req=None
    def setUp(self):
        self.req = buildRequestPost()
        self.sess=kuaisoo.Session(self.req)
        print self.sess['wxid']
    
    def test_save(self):
        self.sess.save()
        self.assertTrue(True )
    def test_load(self):
        wx_id='oaEn2jhk1nCu9VREAmtTDufQd5kw'
        sess=kuaisoo.Session.load_session(self.req)
        print "wxid%s"%sess['wxid']
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()