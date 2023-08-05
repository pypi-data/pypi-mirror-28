# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/12/23.
# ---------------------------------
import json
import time
import os
import qconf_py
import  traceback
class AtmFrame(object):
    def __init__(self,path,request):
        path,self.node=path.split(":")
        path=path.strip("/")
        path,self.version="/".join(path.split("/")[:-1]),path.split("/")[-1]
        print os.path.join("/atmjs/worknew/",path,"main"),self.version,self.node
        self.conf=json.loads(qconf_py.get_conf(os.path.join("/atmjs/worknew/",path,"main")))
        self.path_=path
        self.setting=self.conf.get("settings",None)
        self.maps=self.conf.get("maps",None)
        self.debug=False
        self.debug_domain="//127.0.0.1"
        self.debug_port=""
        self.timestamp=int(time.time())
        try:
            getinfo=request.GET
            debugparams=getinfo[self.setting["debugParam"]]
            self.debug_port=str(self.setting["port"])
            if debugparams:
                self.debug=True
                if debugparams!='true':
                    self.debug_domain=debugparams
            else:
                pass
        except:
            pass
    def transform(self,code):
        if self.debug==True:
            return  code.replace("{{host}}",self.debug_domain+":"+self.debug_port).replace("{{timestamp}}",str(self.timestamp))
        else:
            return  code
    def get_css(self):
        try:
            if self.debug==True:
                return  self.transform(self.maps[self.version][self.path_+":"+self.node]["debug"]["css"])
            else:
                return  self.transform( self.maps[self.version][self.path_+":"+self.node]["formal"]["css"])
        except:
            return ''

    def get_js(self):
        try:
            if self.debug==True:
                return  self.transform(self.maps[self.version][self.path_+":"+self.node]["debug"]["js"])
            else:
                return  self.transform(self.maps[self.version][self.path_+":"+self.node]["formal"]["js"])
        except:
            return ''


import datetime
from django import  template
register=template.Library()
class AtmJsNode(template.Node):
    def __init__(self,path):
        self.path=path
    def render(self, context):
        try:
            request=context["request"]
            return AtmFrame(self.path,request).get_js()
        except Exception as e :
            traceback.print_exc()
            return  str(e),"PATH:%s"%self.path


class AtmCssNode(template.Node):
    def __init__(self,path):
        self.path=path
    def render(self, context):
        try:
            request=context["request"]
            return AtmFrame(self.path,request).get_css()
        except Exception as e :
            traceback.print_exc()
            return  str(e),"PATH:%s"%self.path

@register.tag("atmjs")
def  atmjs_handle(parser,token):
    try:
        tag_name,path=token.split_contents()
    except:
        return ''
    else:
        return AtmJsNode(path)

@register.tag("atmcss")
def atmcss_handle(parser,token):
    try:
        tag_name,path=token.split_contents()
    except:
        return ''
    else:
        return AtmCssNode(path)