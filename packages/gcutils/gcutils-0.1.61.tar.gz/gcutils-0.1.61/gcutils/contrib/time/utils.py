# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/20.
# ---------------------------------
import  datetime
import  time
def get_today_leave_seconds():
    "获取今天剩余的秒数"
    now=datetime.datetime.now()
    _oneday=datetime.timedelta(days=1)
    _u=time.strptime((now+_oneday).strftime("%Y%m%d"),"%Y%m%d")
    return int(time.mktime(_u)-time.time())

def get_tomorrow_leave_seconds():
    "获取到明天剩余的秒数"
    return   86400+get_today_leave_seconds()

def get_week_leave_seconds():
    "获取本周剩余的秒数"
    now_datetime=datetime.datetime.now()
    today_zeroclock_date= now_datetime.strptime(now_datetime.strftime("%Y%m%d"),"%Y%m%d")

    date_list=[today_zeroclock_date+datetime.timedelta(days=i) for i in range(1,9)]
    for i in date_list:
        if i.strftime("%w") =="1" :   #如果为周一
            return int(time.mktime(i.timetuple())-time.time())
def get_month_leave_seconds():
    "获取本月剩余的秒数"
    now_datetime=datetime.datetime.now()
    oneday=datetime.timedelta(days=1)
    _u=1
    while 1:
        nextmonth=now_datetime+oneday*_u
        if nextmonth.day==1:
            break
        else:
            _u+=1
    nextmonth=datetime.datetime.strptime(nextmonth.strftime("%Y%m") ,"%Y%m")
    return  int(time.mktime(nextmonth.timetuple())-time.mktime(now_datetime.timetuple()))