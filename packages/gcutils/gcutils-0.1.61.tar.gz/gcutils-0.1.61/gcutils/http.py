# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/27.
# ---------------------------------
import urllib2
import  urllib
import  json

def _post_json_by_urllib(url,jsondata):
    request=urllib2.Request(url,jsondata)
    request.add_header("Content-type","application/json")
    request.get_method=lambda :"POST"
    request=urllib2.urlopen(request)
    return request.read()

class Api(object):
    def __init__(self,url):
        self.url=url

    def get(self,data={}):
        assert type(data)==dict
        data=dict([((key if type(key)!=unicode else key.encode("utf-8")) ,(v if type(v)!=unicode else v.encode("utf-8")) )  for key,v in data.items()])
        querystring=urllib.urlencode(data)
        if "?" not in self.url:
            url=self.url+"?"+querystring
        else:
            url=self.url+'&'+querystring
        try:
            fd=urllib2.urlopen(url)
            data=fd.read()
            return (True,data)
        except Exception as e :
            return  (False,str(e))
    def post(self,data={},is_json=False):
        assert type(data)==dict
        data=dict([((key if type(key)!=unicode else key.encode("utf-8")) ,(v if type(v)!=unicode else v.encode("utf-8")) )  for key,v in data.items()])
        if is_json==False:
            data=urllib.urlencode(data)
            try:
                #req = urllib2.Request(self.url,data)
                data=urllib2.urlopen(self.url,data,timeout=3)
                return (True,data.read())
            except Exception as e :
                return  (False,str(e))
        else:
            try:
                data=json.dumps(data)
                result=_post_json_by_urllib(self.url,data)
                return  (True,result)
            except Exception as e :
                return  (False,str(e))

# a=Api('http://tj.yw.gongchang.com/api/visitors/')
# data=a.post({"UID":1})
# #print data.decode('utf-8')
# print  data[1]
# print json.loads(data[1])
