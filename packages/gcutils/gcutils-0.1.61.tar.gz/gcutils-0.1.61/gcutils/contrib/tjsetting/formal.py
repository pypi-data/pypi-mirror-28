# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/11/12.
# ---------------------------------

DATABASES = {
    # --------------统计默认数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'statis_v3',                      # Or path to database file if using sqlite3.
        'USER': 'statis',                      # Not used with sqlite3.
        'PASSWORD': 'statis895316',                  # Not used with sqlite3.
        'HOST': '172.17.18.5',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    },
    # ----------------研发cateid对应表所在数据库
    'cate': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gccateinfo',                      # Or path to database file if using sqlite3.
        'USER': 'tj',                      # Not used with sqlite3.
        'PASSWORD': 'jf(w#r82_MHf',                  # Not used with sqlite3.
        'HOST': '172.17.18.4',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    },
    # ----------------pdcheck所在表所在数据库
    'pdcheck': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hlbr',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'gc895316',                  # Not used with sqlite3.
        'HOST': '172.17.13.112',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3307',                      # Set to empty string for default. Not used with sqlite3.
    },
}
API_REDIS={"main":{
            "host":"172.17.21.8",
            "port":6379,
            "db":0,
            "password":"crs-kd38usm2:gc7232275"
          },
          "slave":{
            "host":"172.17.21.8",
            "port":6379,
            "db":0,
              "password":"crs-kd38usm2:gc7232275"
          }
}
CACHE_REDIS={
    "main":{
        "host":"172.17.21.8",  #高可用  后端为   172.17.13.109   172.17.13.110
        "port":6379,
        "db":0,
        "password":"crs-kd38usm2:gc7232275"
    },
    "slave":{
        "host":"172.17.21.8",
        "port":6379,
        "db":0,
        "password":"crs-kd38usm2:gc7232275"
    }
}

#  -------------------------  #################
KAFKA={
    "http":{
        "hosts":"172.17.16.102:9092,172.17.16.106:9092",
        "topic":"statis-detailinfo-collect"
    },
    "socket":{
        "hosts":"172.17.16.102:9092,172.17.16.106:9092",
        "topic":"statis-baseinfo-serverevent"
    },
    "pageevent":{
        "hosts":"172.17.16.102:9092,172.17.16.106:9092",
        "topic":"statis-detailinfo-pageevent"
    }
}
RMQ={"host":"172.17.16.103","port":5672,"user":"admin","passwd":"gc7232275"}

HBASE_CONFIG={
     "main":
         {
        "host":"172.17.17.3",
        "port":9090
         },
     "slave":{
        "host":"172.17.17.3",
        "port":9090
     }
}