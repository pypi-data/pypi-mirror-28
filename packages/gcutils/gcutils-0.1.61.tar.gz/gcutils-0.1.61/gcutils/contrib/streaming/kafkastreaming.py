# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/20.
# ---------------------------------
from kafka import  KafkaConsumer
import  multiprocessing
import  time
import traceback
from collections import  defaultdict
from threading import  Thread,Lock
def function(config):
    handle=config[0]
    info=config[1]
    while 1:
        try:
            handle(info)
        except Exception as e :
            time.sleep(0.01)
            traceback.print_exc()
        else:
            break
class StreamConsumer(object):
    "队列消费类抽象"
    def __init__(self,hosts,topic,group,begin="largest",commit=True):
        self.hosts=hosts
        self.topic=topic
        self.group=group
        self.functionlist=[]
        self.begin=begin
        self.commit=commit
        pass
    def decorator(self,funcion):
        self.functionlist.append(funcion)
        return  funcion

    def run(self,message_handler=None):
        "参数说明： message_handler是用来对接受到的消息进行初步的筛选处理的函数"
        assert len(self.functionlist)!=0
        processpool=multiprocessing.Pool(len(self.functionlist))
        _consumer=KafkaConsumer(self.topic,bootstrap_servers=self.hosts.split(","),auto_offset_reset=self.begin,auto_commit_enable=False,group_id=self.group)
        for message in _consumer:
            info=message.value
            try:
                info=info.decode("utf-8")
            except:
                continue
            else:
                pass
            if message_handler!=None:
                try:
                    info=message_handler(info)
                except:
                    _consumer.task_done(message)
                    if message.offset%50==0:
                        _consumer.commit()
                    continue
                else:
                    pass
            processpool.map(function,zip(self.functionlist,[info]*len(self.functionlist)))
            _consumer.task_done(message)
            if self.commit==True:
                _consumer.commit()

class BatchStreamConsumer(object):
    "队列消费类抽象"
    def __init__(self,hosts,topic,group,begin="largest",commit=True,batchsize=1):
        '''
        hosts      主机
        topic      队列名
        group      消费者组名
        batchsize  窗口时间，秒。   默认为1 '''
        self.hosts=hosts
        self.topic=topic
        self.group=group
        self.functionlist=[]
        self.begin=begin
        self.commit=commit
        self.batchsize=batchsize

    def decorator(self,funcion):
        self.functionlist.append(funcion)
        return  funcion

    def run(self,message_handler=None):
        "参数说明： message_handler是用来对接受到的消息进行初步的筛选处理的函数"
        assert len(self.functionlist)!=0
        processpool=multiprocessing.Pool(len(self.functionlist))
        lock=Lock()
        _consumer=KafkaConsumer(self.topic,bootstrap_servers=self.hosts.split(","),auto_offset_reset=self.begin,auto_commit_enable=False,group_id=self.group)
        self.infolist=[]
        self.timeclock=0
        def check_fun():
            while 1:
                time.sleep(0.02)
                lock.acquire()
                if time.time()-self.timeclock>self.batchsize:
                    if len(self.infolist)>0:
                        processpool.map(function,zip(self.functionlist,[self.infolist]*len(self.functionlist)))
                        self.infolist=[]
                        self.timeclock=time.time()
                    else:
                        pass
                    if self.commit and self.timeclock:
                        _consumer.commit()
                lock.release()
        _thread=Thread(target=check_fun)
        _thread.start()
        for message in _consumer:
            lock.acquire()
            info=message.value
            try:
                info=info.decode("utf-8")
            except:
                continue
            else:
                pass
            if message_handler!=None:
                try:
                    info=message_handler(info)
                except:
                    pass
                else:
                    self.infolist.append(info)
            _consumer.task_done(message)
            lock.release()

import  sqlite3

class SqlBatchStreamConsumer(object):
    "队列消费类抽象"
    def __init__(self,hosts,topic,group,begin="largest",tablename=None,commit=True,batchsize=1):
        '''
        hosts      主机
        topic      队列名
        group      消费者组名
        batchsize  窗口时间，秒。   默认为1 '''
        self.hosts=hosts
        self.topic=topic
        self.group=group
        self.sqllist=[]
        self.begin=begin
        self.commit=commit
        self.batchsize=batchsize
        self.tablename=tablename if tablename!=None  else self.topic
        self.conn=None
        self.tablecreate=False
        self._udflist=[]

    def add_sql_handle(self,sql):
        "添加batch  handle sql"
        self.sqllist.append(sql)


    def register_function(self,name,num_params,func):
        "注册 自定义函数"
        self._udflist.append([name,num_params,func])


    def run(self,message_handler=None):
        "参数说明： message_handler是用来对接受到的消息进行初步的筛选处理的函数"
        assert len(self.sqllist)!=0
        lock=Lock()
        _consumer=KafkaConsumer(self.topic,bootstrap_servers=self.hosts.split(","),auto_offset_reset=self.begin,auto_commit_enable=False,group_id=self.group)
        self.infolist=[]
        self.timeclock=0
        def check_fun():
            while 1:
                time.sleep(0.02)
                lock.acquire()
                if time.time()-self.timeclock>self.batchsize:
                    if len(self.infolist)>0:
                        _columns=tuple(self.infolist[0].keys())
                        _infolist=[ tuple([unicode(i.get(column,''))   for column in _columns] ) for i in self.infolist ]
                        if self.conn==None:
                            self.conn=sqlite3.connect(":memory:")
                            for name,num_params,func  in self._udflist:
                                self.conn.create_function(name,num_params,func)
                        else:
                            pass
                        cur=self.conn.cursor()
                        if self.tablecreate==False:
                            cur.execute("create table " +self.tablename+ "(  " +  "  , ".join([i+" TEXT "  for i in _columns])+")")
                            self.tablecreate=True
                        else:
                            pass
                        cur.executemany("insert into "+self.tablename+" values %s"%(str(tuple(["?"]*_columns.__len__())).replace("'",'')),_infolist)
                        for sql  in self.sqllist:
                            cur.execute(sql)
                            print "sql:",sql
                            print "sql result:",cur.fetchall()
                        cur.execute("delete from  "+self.tablename)
                        cur.close()
                        self.infolist=[]
                        self.timeclock=time.time()
                    else:
                        pass
                    if self.commit and self.timeclock:
                        _consumer.commit()
                lock.release()
        _thread=Thread(target=check_fun)
        _thread.start()
        for message in _consumer:
            lock.acquire()
            info=message.value
            try:
                info=info.decode("utf-8")
            except:
                continue
            else:
                pass
            if message_handler!=None:
                try:
                    info=message_handler(info)
                except:
                    pass
                else:
                    self.infolist.append(info)
            else:
                self.infolist.append(info)
            _consumer.task_done(message)
            lock.release()



