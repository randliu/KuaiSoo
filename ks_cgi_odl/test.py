#!/usr/bin/python
#coding=utf-8  
import subprocess
import os
import ks_http
"""
INFO:root.test:<b>     REDIRECT_STATUS</b>: 200<br>
INFO:root.test:<b>     SERVER_SOFTWARE</b>: LiteSpeed<br>
INFO:root.test:<b>         SCRIPT_NAME</b>: /scgi-bin/handler.py<br>
INFO:root.test:<b>      REQUEST_METHOD</b>: POST<br>
INFO:root.test:<b>     SERVER_PROTOCOL</b>: HTTP/1.0<br>
INFO:root.test:<b>        QUERY_STRING</b>: signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928<br>
INFO:root.test:<b>      CONTENT_LENGTH</b>: 240<br>
INFO:root.test:<b>     HTTP_USER_AGENT</b>: Mozilla/4.0<br>
INFO:root.test:<b>     HTTP_CONNECTION</b>: Keep-Alive<br>
INFO:root.test:<b>         SERVER_NAME</b>: www.kuaisoo.net<br>
INFO:root.test:<b>         REMOTE_PORT</b>: 48295<br>
INFO:root.test:<b>         SERVER_PORT</b>: 80<br>
INFO:root.test:<b>         SERVER_ADDR</b>: 216.24.245.126<br>
INFO:root.test:<b>       DOCUMENT_ROOT</b>: /home/kuaisoon/public_html<br>
INFO:root.test:<b>         HTTP_PRAGMA</b>: no-cache<br>
INFO:root.test:<b>     SCRIPT_FILENAME</b>: /home/kuaisoon/public_html/scgi-bin/handler.py<br>
INFO:root.test:<b>        SERVER_ADMIN</b>: webmaster@kuaisoo.net<br>
INFO:root.test:<b>           HTTP_HOST</b>: www.kuaisoo.net<br>
INFO:root.test:<b>         REQUEST_URI</b>: /scgi-bin/handler.py?signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928<br>
INFO:root.test:<b>         HTTP_ACCEPT</b>: */*<br>
INFO:root.test:<b>   GATEWAY_INTERFACE</b>: CGI/1.1<br>
INFO:root.test:<b>         REMOTE_ADDR</b>: 101.226.89.83<br>
INFO:root.test:<b>        CONTENT_TYPE</b>: text/xml<br>
"""
text_msg=u"""<xml><ToUserName><![CDATA[gh_1ff87fe87f88]]></ToUserName>
<FromUserName><![CDATA[oaEn2jhk1nCu9VREAmtTDufQd5kw]]></FromUserName>
<CreateTime>1356344005</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[大小]]></Content>
</xml>"""

img_msg="""<xml><ToUserName><![CDATA[gh_1ff87fe87f88]]></ToUserName>
<FromUserName><![CDATA[oaEn2jhk1nCu9VREAmtTDufQd5kw]]></FromUserName>
<CreateTime>1356344005</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[?]]></Content>
</xml>"""

os.environ['REQUEST_METHOD']='POST'
os.environ['QUERY_STRING']='signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928&echostr=tfffff'
os.environ['REQUEST_URI']='/scgi-bin/handler.py?signature=840e8ee35ef65dd598f1c5f249fa213801fdf6d4&timestamp=1356517202&nonce=1355917928'
script = "/Users/user/Documents/workspace/KuaiSoo/ks_cgi/handler.py"
child = subprocess.Popen(['python',script], stdin=subprocess.PIPE)
child.communicate(text_msg)