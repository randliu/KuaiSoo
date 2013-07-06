# -*- coding: utf-8 -*- 

import urllib2, urllib

search_key_word = u"申通 福州"

#query = urllib.urlencode({'q' : search_key_word.encode("utf-8")+' site:www.tianya.cn','rsz':'large',})
query = urllib.urlencode({'q' : search_key_word.encode("utf-8"),'rsz':'small',})

url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s '% (query)
search_results = urllib.urlopen(url)
        
content=search_results.read()
search_results.close()
print content
