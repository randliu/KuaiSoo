#!/usr/bin/python
#coding=utf-8
q=None
start = 0
web_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&start=%s'

"""
"cursor": {
      "resultCount": "143,000",
      "pages": [
        {
          "start": "0",
          "label": 1
        },
        ... ..
        {
          "start": "28",
          "label": 8
        }
      ],
      "estimatedResultCount": "143000",
      "currentPageIndex": 0,
      "moreResultsUrl": "http://www.google.com/search?oe\u003dutf8\u0026ie\u003dutf8\u0026source\u003duds\u0026start\u003d0\u0026hl\u003dzh-CN\u0026q\u003dabc123",
      "searchResultTime": "0.15"
    }
"""

class page:
    start = 0
    label = 1
    
class cursor:
    resultCount = 0
    pages=[]
    estimatedResultCount = 0
    currentPageIndex = 0
    moreResultsUrl=""
    searchResultTime=0
    
class GoogleWebResult:
    #search_type="web"   #images
    GsearchResultClass = 'GwebSearch'
    unescapedUrl=''
    url = ''
    visibleUrl = ''
    cacheUrl=''
    title=''
    titleNoFormatting = ''
    content=''
class GoogleWebResponse:
    results = [] # list of GoogleWebResult
    cursor=None
    responseDetails = None
    responseStatus=200
    