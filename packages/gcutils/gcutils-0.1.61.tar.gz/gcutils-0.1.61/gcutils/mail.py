# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/15.
# ---------------------------------
import smtplib
from email.mime.text import  MIMEText
from email.header import  Header

def sendmail(receiver,text,sender,server,password):
    msg = MIMEText('<html><h1>%s</h1></html>'%text,'html','utf-8')
    smtp=smtplib.SMTP()
    smtp.connect(server)
    smtp.login(sender,password)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.close()