# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/15.
# ---------------------------------
from mode import Singleton
import redis, datetime
from gcutils.queue import KafkaMgr
import json
import MySQLdb
import urllib2
import  base64
import  consul
from ctypes import  *
from gcutils.encrypt import md5
import  time

class _RedisMgrSingleton(type):
    def __init__(self, name, bases, dict):
        super(_RedisMgrSingleton, self).__init__(name, bases, dict)
        self._instance = {}

    def __call__(self, host, port, db,password=None):
        if not self._instance.has_key((host, port, db)):
            self._instance[(host, port, db)] = super(_RedisMgrSingleton, self).__call__(host, port, db,password)
        return self._instance[(host, port, db)]


class RedisMgr:
    "redis操作专用类"

    def __init__(self, host, port, db,password, max_connections=3):
        "eg:  host    '192.168.2.184'   port  6379    db   14"
        self.host = host
        self.port = port
        self.db = db
        self.password=password
        if not self.password:
            self.conn = redis.Redis(
                    connection_pool=redis.ConnectionPool(host=host, port=port, db=db, max_connections=max_connections))
        else:
            self.conn = redis.Redis(
                    connection_pool=redis.ConnectionPool(host=host, port=port, db=db,password=self.password ,max_connections=max_connections))

    def run_redis_fun(self, funname, *args):
        fun = getattr(self.conn, funname)
        return fun(*args)

    __metaclass__ = _RedisMgrSingleton


class MySQLMgr(object):
    def __init__(self, host, port, db, user, passwd):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd

    def runQuery(self, sql, args):
        if ("select" not in sql) and ("SELECT" not in sql):
            return ()
        else:
            conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
                                   charset="utf8")
            cursor = conn.cursor()
            cursor.execute(sql, args)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result

    def runOperation(self, sql, args, withpaimarykey=False):
        conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
                               charset="utf8")
        cursor = conn.cursor()
        rows = cursor.execute(sql, args)
        cursor.close()
        conn.commit()
        conn.close()
        if withpaimarykey == True:
            return int(rows), int(cursor.lastrowid)
        else:
            return int(rows)


def _post_json_by_urllib(url, jsondata):
    request = urllib2.Request(url, jsondata)
    request.add_header("Content-type", "application/json")
    request.get_method = lambda: "POST"
    request = urllib2.urlopen(request)
    return request.read()


class SolrMgr(object):
    def __init__(self, host, port, region):
        self.host = host
        self.port = port
        self.region = region

    def post_json(self, dictdata):
        result = _post_json_by_urllib("http://%s:%s/solr/%s/update" % (self.host, self.port, self.region),
                                      json.dumps(dictdata, ensure_ascii=False).encode("utf-8"))
        status = json.loads(result)
        if status["responseHeader"]["status"] == 0:
            return True
        else:
            return False


class _SyncSolrMgrSingleton(type):
    def __init__(self, name, bases, dict):
        super(_SyncSolrMgrSingleton, self).__init__(name, bases, dict)
        self._instance = {}

    def __call__(self, host, port, regions, kafkahosts, kafkatopic):
        if not self._instance.has_key((host, port, regions, kafkahosts, kafkatopic)):
            self._instance[(host, port, regions, kafkahosts, kafkatopic)] = super(_SyncSolrMgrSingleton, self).__call__(
                    host, port, regions, kafkahosts, kafkatopic)
        return self._instance[host, port, regions, kafkahosts, kafkatopic]


class SyncSolrMgr(object):
    "异步提交数据到solr"
    __metaclass__ = _SyncSolrMgrSingleton

    def __init__(self, host, port, region, kafkahosts, kafkatopic):
        self.host = host
        self.port = port
        self.region = region
        self.kafkatopic = kafkatopic
        self.kafkahosts = kafkahosts
        self.kafka = KafkaMgr(kafkahosts)

    def put(self, dictdata):
        data = {"host": self.host, "port": self.port, "region": self.region, "data": dictdata}
        return self.kafka.send_message(self.kafkatopic, json.dumps(data, ensure_ascii=False))


class _SyncHbaseMgrSingleton(type):
    def __init__(self, name, bases, dict):
        super(_SyncHbaseMgrSingleton, self).__init__(name, bases, dict)
        self._instance = {}

    def __call__(self, host, table, kafkahosts, kafkatopic):
        assert isinstance(kafkahosts, (str, unicode))
        if not self._instance.has_key((host, table, kafkahosts, kafkatopic)):
            self._instance[(host, table, kafkahosts, kafkatopic)] = super(_SyncHbaseMgrSingleton, self).__call__(host,
                                                                                                                 table,
                                                                                                                 kafkahosts,
                                                                                                                 kafkatopic)
        return self._instance[host, table, kafkahosts, kafkatopic]


class SyncHbaseMgr:
    "hbase操作专用类"
    __metaclass__ = _SyncHbaseMgrSingleton

    def __init__(self, host, table, kafkahosts, kafkatopic):
        '''eg： host        '192.168.2.184'    hbase的host
                table       'statis'        hbase的表名
                kafkahosts  '192.168.3.1:9092,192.168.3.2:9092'   kafka集群的hosts配置
                kafkatopic  'put_hbase'     对应的kafka的topic
         '''
        assert isinstance(kafkahosts, (str, unicode))
        self.host = host
        self.kafka = KafkaMgr(kafkahosts)
        self.table = table
        self.kafkatopic = kafkatopic
        self.kafkahosts = kafkahosts

    def put(self, rowkey, data):
        _data = json.dumps({"rowkey": str(rowkey), "data": data, "table": self.table}, ensure_ascii=False)
        if type(_data) == unicode:
            _data = _data.encode("utf-8")
        return self.kafka.send_message(self.kafkatopic, _data)

    def batch_put(self, rowkey, data):
        "批量操作hbase，put"
        if hasattr(self, "batch"):
            self.batch.append((rowkey, data))
        else:
            self.batch = [(rowkey, data)]

    def batch_commit(self):
        '批量操作Hbase , commit'
        if hasattr(self, "batch"):
            args = [json.dumps({"rowkey": str(rowkey), "data": data, "table": self.table}) for rowkey, data in
                    self.batch]
            self.kafka.send_message(self.kafkatopic, *args)
        else:
            pass

class _Consul(type):

    def __init__(self, name, bases, dict):
        super(_Consul, self).__init__(name, bases, dict)
        self._instance = {}

    def __call__(self, server="127.0.0.1", port=8500):
        assert isinstance(server, (str, unicode))
        assert  isinstance(port,int)
        if not self._instance.has_key((server,port)):
            self._instance[(server,port)] = super(_Consul, self).__call__(server,port)
        return self._instance[(server,port)]

class ConsulMgr:
    "consul kv 读写类"
    __metaclass__ = _Consul
    rt=CDLL("librt.so")
    shmget=rt.shmget
    shmget.argtypes = [c_int, c_size_t, c_int]
    shmget.restype = c_int
    shmat = rt.shmat
    shmat.argtypes = [c_int, POINTER(c_void_p), c_int]
    shmat.restype = c_void_p
    memcpy=rt.memcpy
    memcpy.argtypes=[c_void_p,c_void_p,c_int]
    memcpy.restype=c_void_p
    shmid = shmget(0x13ffdd13,1024*1024*130, 0o666|001000)
    addr=shmat(shmid,None,0)

    def __init__(self, server="127.0.0.1",port=8500):
        self._server = server
        self._port=port
        self._server_url="http://%s:%s"%(server,port)
        self.consul=consul.Consul(server,port)

    def kv_get(self, key):
        '''
        获取Kv 值
        :param key: 键
        :return string or None  如果键存在则返回其值，否则返回None
        '''
        try:
            _mem_result= self._cache_get(key,flag="$$-kv-$$-")
            if _mem_result:
                data= _mem_result
            else:
                try:
                    data=urllib2.urlopen("%s/v1/kv/%s"%(self._server_url,key)).read()
                except:
                    data=json.dumps([{"Value":None}])
                self._cache_reset(key,data,flag="$$-kv-$$-")
            result=  base64.b64decode(json.loads(data)[0]["Value"])
            return result
        except  :
            return  None
    def _cache_get(self,key,flag=''):
        offset=eval("0x"+ md5(flag+key)[8:24])%10000*1024*13
        _key=string_at(self.addr+offset,1024).strip("\x00")
        value=string_at(self.addr+offset+1024,1024*10).strip("\x00")
        timestamp=string_at(self.addr+offset+1024*11,1024).strip("\x00")
        hash=string_at(self.addr+offset+1024*12,1024).strip("\x00")
        if md5(key+value+timestamp)==hash[1:] and int(timestamp)==int(time.time()) and hash[0]=="1" and key==_key :
            return value
        else:
            return None

    def _cache_reset(self,key,value,flag=""):
        if len(key)<=1024 and len(value)<=1024*10:
            offset=eval("0x"+ md5(flag+key)[8:24])%10000*1024*13
            _fill=lambda _str,_len:_str+(_len-len(_str))*"\x00"
            _timestamp=str(int(time.time()))
            content=_fill(key,1024)+_fill(value,1024*10)+_fill(_timestamp,1024)+_fill("1"+md5(key+value+_timestamp),1024)
            content=c_char_p(content)
            self.memcpy(cast(self.addr+offset,c_void_p) ,content,1024*13)

    def service_get(self, service):
        '''
        获取一个service的信息
        :param service   服务名
        :return dict or None 如果服务存在则返回dict，否则返回None,如：
        [{u'Node': u'hadoop95', u'ServiceName': u'test', u'ModifyIndex': 20890, u'ServicePort': 3306,
            u'ServiceID': u'test', u'ServiceAddress': u'192.168.8.94', u'Address': u'192.168.8.95',
            u'ServiceTags': [u'test11'], u'CreateIndex': 396, u'ServiceEnableTagOverride': False},
         {u'Node': u'hadoop96', u'ServiceName': u'test', u'ModifyIndex': 11998, u'ServicePort': 3306,
            u'ServiceID': u'test', u'ServiceAddress': u'192.168.8.94', u'Address': u'192.168.8.96',
            u'ServiceTags': [u'test'], u'CreateIndex': 376, u'ServiceEnableTagOverride': False}]
        '''
        try:
            flag="$$-service-$$$$$~~"
            _mem_result=self._cache_get(service,flag=flag)
            try:
                _mem_result=json.loads(_mem_result)
            except:
                _mem_result=None
            if _mem_result:
                result=_mem_result
            else:
                try:
                    result=urllib2.urlopen("%s/v1/catalog/service/%s"%(self._server_url,service)).read()
                except:
                    result=json.dumps([])
                self._cache_reset(service,result,flag)
                result=json.loads(result)
            assert  result[1]!=[]
            return  result[1]
        except:
            return  None

    def service_all(self):
        '''
        获取所有service的名称
        :return list  or None   如：[u'test', u'consul', u'tj.gongchang.com/test/aa/', u'tj.gongchang.com.test']
        '''
        try:
            flag="$$$$$$*/54dservice-all-$$$"
            _mem_result=self._cache_get("service-all",flag=flag)
            try:
                _mem_result=json.loads(_mem_result)
            except:
                _mem_result=None
            if _mem_result:
                result=_mem_result
            else:
                result=self.consul.catalog.services()
                self._cache_reset("service-all",json.dumps(result),flag)
            assert  result[1].keys()!=[]
            return result[1].keys()
        except:
            return  None

    def node_get(self,node):
        '''
        获取一个node的信息
        :param node  节点名
        :return  dict or None  如：
        {u'Node': {u'Node': u'hadoop95', u'TaggedAddresses': {u'wan': u'192.168.8.95'}, u'ModifyIndex': 20897, u'CreateIndex': 6, u'Address': u'192.168.8.95'},
        u'Services': {u'test': {u'Service': u'test', u'Tags': [u'test11'], u'ModifyIndex': 20890,
                                u'EnableTagOverride': False, u'ID': u'test', u'Address': u'192.168.8.94',
                                u'CreateIndex': 396, u'Port': 3306},
                      u'tj.gongchang.com/test/aa/': {u'Service': u'tj.gongchang.com/test/aa/', u'Tags': [u'test11'],
                                 u'ModifyIndex': 20874, u'EnableTagOverride': False, u'ID': u'tj.gongchang.com/test/aa/',
                                 u'Address': u'192.168.8.94', u'CreateIndex': 456, u'Port': 3306},
                      u'tj.gongchang.com.test': {u'Service': u'tj.gongchang.com.test', u'Tags': [u'test11'],
                                 u'ModifyIndex': 20897, u'EnableTagOverride': False, u'ID': u'tj.gongchang.com.test',
                                 u'Address': u'192.168.8.94', u'CreateIndex': 447, u'Port': 3306},
                      u'tj.gongchang.com': {u'Service': u'tj.gongchang.com', u'Tags': [u'test1'], u'ModifyIndex': 20888,
                                            u'EnableTagOverride': False, u'ID': u'tj.gongchang.com',
                                            u'Address': u'192.168.8.94', u'CreateIndex': 474, u'Port': 3307}}
                      }
        '''
        try:
            flag="$$#@DWERW-node-##"
            _mem_result=self._cache_get(node,flag=flag)
            try:
                _mem_result=json.loads(_mem_result)
            except:
                _mem_result=None
            if _mem_result:
                result=_mem_result
                #print "from cache"
            else:
                result=self.consul.catalog.node(node)
                self._cache_reset(node,json.dumps(result),flag)
            assert  result[1]!=None
            assert  isinstance(result[1],dict)
            return  result[1]
        except:
            return  None

    def node_all(self):
        '''
        获取所有Node的信息
        :return list or None . 如：
        [{u'Node': u'hadoop94', u'TaggedAddresses': {u'wan': u'192.168.8.94'},
                                        u'ModifyIndex': 307, u'CreateIndex': 5, u'Address': u'192.168.8.94'},
         {u'Node': u'hadoop95', u'TaggedAddresses': {u'wan': u'192.168.8.95'},
                                        u'ModifyIndex': 20897, u'CreateIndex': 6, u'Address': u'192.168.8.95'},
         {u'Node': u'hadoop96', u'TaggedAddresses': {u'wan': u'192.168.8.96'},
                                        u'ModifyIndex': 11998, u'CreateIndex': 3, u'Address': u'192.168.8.96'}]
        '''
        try:
            flag="$#$%@#0-nodeall-##"
            _mem_result=self._cache_get("node-all",flag=flag)
            try:
                _mem_result=json.loads(_mem_result)
            except:
                _mem_result=None
            if _mem_result:
                result=_mem_result
            else:
                result=self.consul.catalog.nodes()
                print len(json.dumps(result))
                self._cache_reset("node-all",json.dumps(result),flag)
            assert  result[1]!=[]
            return  result[1]
        except:
            return  None


# obj=ConsulMgr("192.168.8.96")
# aa=[]
# print time.time()
# for i in range(0,30000):
#     #aa.append([ obj.kv_get("test"),obj.node_get("hadoop96"),obj.node_all(),obj.service_get("test"),obj.service_all()])
#     aa.append([obj.node_all()])
# print aa[-10:]
# print time.time()