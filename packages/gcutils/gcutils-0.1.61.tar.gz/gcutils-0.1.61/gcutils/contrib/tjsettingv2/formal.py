# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/11/12.
# ---------------------------------
#################################################################################################
V2_MYSQL={"tongji":{
            "host":"172.17.18.5",
            "port":3306,
            "user":"statis",
            "passwd":"statis895316"
          },
          "yf":{
              "host":"172.17.18.4",
              "port":3306,
              "user":"tj",
              "passwd":"jf(w#r82_MHf"
          },
          "yf_cj":{
              "host":"172.17.18.6",
              "port":3306,
              "user":"tj",
              "passwd":"jf(w#r82_MHf"
          },
          "yf_tjslave":{
              "host":"172.17.19.102",
              "port":3306,
              "user":"tj",
              "passwd":"jf(w#r82_MHf"
          },
          "hlbr":{
              "host":"172.17.13.112",
              "port":3307,
              "user":"root",
              "passwd":"gc895316"
          }}
V2_SPHINX={
    "product":{
        "host":"172.17.17.105",
        "port":9093
    }
}
V2_REDIS={"api":{
            "host":"172.17.21.8",
            "port":6379,
            "db":0,
            "password":"crs-kd38usm2:gc7232275"
          },
          "cache":{
            "host":"172.17.21.8",
            "port":6379,
            "db":0,
              "password":"crs-kd38usm2:gc7232275"
          }
}
V2_KAFKA={
    "hosts":"172.17.16.102:9092,172.17.16.106:9092"
}
V2_RMQ={"host":"172.17.16.103","port":5672,"user":"admin","passwd":"gc7232275"}

V2_HBASE={
        "host":"172.17.17.3",
        "port":9090
}

V2_MONGO={"host":"172.17.13.111",
          "port":27017}


V2_SERVER_COMMON="172.17.13.111"
###################################################################
