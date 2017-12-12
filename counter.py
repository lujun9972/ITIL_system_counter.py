#!/usr/bin/env python3 
# -*- python-shell-interpreter: "python3"; -*-
import csv
import sys
from collections import Counter
import calendar
from datetime import datetime

def read_file(file):
    '''读取FILE的内容,转换成dict列表,且将其中的计划开始时间转换成datetime格式'''
    with open(file,encoding='gbk') as f:
        d = csv.DictReader(f)
        d = filter(lambda x:x['变更类别']=='应用变更',d)
        d = filter(lambda x:x['分类一级']=='应用',d)
        d = list(d)
        for i in d:
            i['计划开始时间'] = datetime.strptime(i['计划开始时间'],'%Y-%m-%d %H:%M')
        return list(d)

def filter_by_start_time(d,start,end):
    '''返回D中计划开始时间介于[START,END]的数据列表'''
    d = filter(lambda x:x['计划开始时间']>=start and x['计划开始时间']<=end,d)
    return list(d)

def counter(d):
    '''根据D[分类二级]统计各系统变更量,返回一个各系统统计结果'''
    d = map(lambda x:x['分类二级'],d)
    c = Counter(d)
    return c

def get_week_ranges(year,mon,firstweekday=calendar.THURSDAY):
    '''返回YEAR/MON这个月份中各个week的开始日期和结束日期,FIRSTWEEKDAY指定周几为week的第一天'''
    old_firstweekday = calendar.firstweekday()
    calendar.setfirstweekday(firstweekday)
    c = calendar.monthcalendar(year,mon)
    calendar.setfirstweekday(old_firstweekday)
    c = map(lambda x:list(filter(lambda y:y!=0,x)),c)
    c = map(lambda x:(datetime(year,mon,min(x)),
                      datetime(year,mon,max(x),23,59,59)),c)
    return list(c)

def guess_date(records):
    '''根据记录中的计划开始时间推测要统计的时那一年那个月的数据'''
    start_date = records[0]['计划开始时间']
    year = start_date.year
    month = start_date.month
    return (year,month)

def count_from_file(csv_file):
    '''统计CSV_FILE中的各系统上线数量'''
    records = read_file(csv_file)
    year,mon = guess_date(records)
    week_ranges = get_week_ranges(year,mon)
    d = {}
    for week_range in week_ranges:
        week_records = filter_by_start_time(records,*week_range)
        week_counter = counter(week_records)
        d[week_range] = week_counter
    return d

def output_count(count):
    '''输出统计结果'''
    for week_range,week_counter in count.items():
        print(*week_range)
        for k,v in week_counter.items():
            print(k,",",v)

def Usage():
    print('''Usage:{} CSV_FILE

    注意:CSV_FILE必须是UTF-8格式的'''.format(sys.argv[0]))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        count = count_from_file(sys.argv[1])
        output_count(count)
    else:
        Usage()
