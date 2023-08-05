# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/15.
# ---------------------------------
import  kafka
from pika import  connection,BlockingConnection,ConnectionParameters,credentials,BasicProperties

class _KafkaMgrSingleton(type):
    def __init__(self, name, bases, dict):
        super(_KafkaMgrSingleton, self).__init__(name, bases, dict)
        self._instance = {}
    def __call__(self, hosts):
        if not self._instance.has_key(hosts):
            self._instance[hosts] = super(_KafkaMgrSingleton, self).__call__(hosts)
        return self._instance[hosts]
class KafkaMgr(object):
    "kafka操作类"
    __metaclass__ = _KafkaMgrSingleton
    def __init__(self,hosts):
        "hosts :'192.168.2.184:9092,192.168.2.1:9092'"
        self.hosts=hosts
        self.client=kafka.KafkaClient(hosts,timeout=2851200)
        self.productor=kafka.SimpleProducer(self.client)
    def send_message(self,topic,*messages):
        messages=[(i if isinstance(i,str) else i.encode("utf-8")) for i in messages]
        return self.productor.send_messages(topic,*messages)
    def __del__(self):
        self.client.close()


class KeyedKafkaMgr(object):
    "keyed  kafka操作类"
    __metaclass__ = _KafkaMgrSingleton
    def __init__(self,hosts):
        "hosts :'192.168.2.184:9092,192.168.2.1:9092'"
        self.hosts=hosts
        self.client=kafka.KafkaClient(hosts,timeout=2851200)
        self.productor=kafka.KeyedProducer(self.client)
    def send_message(self,topic,key,*messages):
        messages=[(i if isinstance(i,str) else i.encode("utf-8")) for i in messages]
        return self.productor.send_messages(topic,key,*messages)
    def __del__(self):
        self.client.close()

class _RmqMgrSingleton(type):
    def __init__(self, name, bases, dict):
        super(_RmqMgrSingleton, self).__init__(name, bases, dict)
        self._instance = {}
    def __call__(self, host,port,user,passwd):
        if not self._instance.has_key((host,port,user,passwd)):
            self._instance[(host,port,user,passwd)] = super(_RmqMgrSingleton, self).__call__(host,port,user,passwd)
        return self._instance[(host,port,user,passwd )]
class RmqMgr(object):
    "rabbit mq 队列的一个抽象"
    __metaclass__ = _RmqMgrSingleton
    def __init__(self,host,port,user,passwd):
        self.host=host
        self.port=port
        self.user,self.passwd=user,passwd
    def _get_rmq_channel(self ,host,port,user,passwd,withconn=False):
        "获取连接到rabbitmq的通道对象"
        conn=BlockingConnection(ConnectionParameters(host=host,port=port,credentials=credentials.PlainCredentials(username=user,password=passwd)))
        if withconn==False:
            return  conn.channel()
        else:
            return conn.channel(),conn
    def send_message(self ,exchange,routeing_key,body):
        "发送消息到队列"
        if type(body)==unicode:
            body=body.encode("utf-8")
        assert type(body)==str
        try:
            self.__channel.basic_publish(exchange=exchange,routing_key=routeing_key,body=body,properties=BasicProperties(delivery_mode=2))
        except:
            self.__channel,self.__conn=self._get_rmq_channel(self.host,self.port,self.user,self.passwd,withconn=True)
            self.__channel.basic_publish(exchange=exchange,routing_key=routeing_key,body=body,properties=BasicProperties(delivery_mode=2))
        return True
    def __del__(self):
        self.__conn.close()
