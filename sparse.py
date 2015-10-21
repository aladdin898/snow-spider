# -*- coding: utf-8 -*-
import sys
import os
import MySQLdb
import time
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

CreatDate=time.strftime('%Y-%m-%d %H:%M:%S')
Field1='None'
Field2='None'
Field3='None'

soup = BeautifulSoup(open('index.html'),"lxml")
#print soup.prettify()

stockinfo=soup.find("strong", {"class": "stockName"})
StockCode=stockinfo.string[-10:-8]+stockinfo.string[-7:-1]
StockName=stockinfo.string[:-11]

list = soup.findAll('td')
#for i in range(len(list)):
#    print list[i].span.string
if len(list) != 20:
    print len(list),StockName
    sys.exit()
TodayHigh=list[1].span.string.replace('-','0')
TodayLow=list[5].span.string.replace('-','0')
YearHigh=list[2].span.string.replace('-','0')
YestClose=list[4].span.string.replace('-','0')
YearLow=list[6].span.string.replace('-','0')
UpLimit=list[8].span.string.replace('-','0')
TotalValue=list[9].span.string.replace('-','0亿')[:-1]
Earnings=list[10].span.string
if Earnings==None:
    PerEarnings=0.01
else:
    PerEarnings=Earnings.replace('-','0')
DownLimit=list[12].span.string.replace('-','0')
TotalCapital=list[13].span.string.replace('-','0亿')[:-1]
PerNetAssets=list[14].span.string.replace('-','0')
PBRatio=list[15].span.string.replace('-','0')
FlowCapital=list[17].span.string.replace('-','0亿')[:-1]
PerDividend=list[18].span.string.replace('-','0')
PSRatio=list[19].span.string.replace('-','0')
PERatio=list[11].span.string.replace('-','0').split('/')
LYRPERatio=PERatio[0]
TTMPERatio=PERatio[1]
TodayRange=list[16].span.string.replace('-','0%')[:-1]
TodayOpen=list[0].span.string.replace('-','0')
Volume=list[3].span.string.replace('-','0万股')[:-2]
Turnover=list[7].span.string.replace('-','0万')[:-1]

closeinfo=soup.find("div", {"class": "stock-closed"})
if closeinfo == None:
    HaltFlag=0
    currentInfo=soup.find("div", {"class": "currentInfo"})
    CurrentPrice=currentInfo.strong.string.replace('-','￥0')[1:]
    priceinfo=currentInfo.findAll("span")
    PriceChange=priceinfo[1].string.strip().replace('-','0')
    QuoteChange=priceinfo[2].string.strip()[1:-2]
    timeInfo=soup.find("span", {"id": "timeInfo"})
    Datekey="2015-"+timeInfo.string.strip()[0:5]
    Timekey=timeInfo.string.strip()[6:14]
else:
    HaltFlag=1
    CurrentPrice=YestClose
    PriceChange=0
    QuoteChange=0
    Datekey=CreatDate[0:10]
    Timekey=CreatDate[11:]

#print StockCode
#print StockName
#print Datekey
#print Timekey
#print CurrentPrice
#print PriceChange
#print QuoteChange
#print YestClose
#print TodayOpen
#print TodayHigh
#print TodayLow
#print TodayRange
#print UpLimit
#print DownLimit
#print YearHigh
#print YearLow
#print Volume
#print Turnover
#print TotalValue
#print TotalCapital
#print FlowCapital
#print PerEarnings
#print PerDividend
#print PerNetAssets
#print LYRPERatio
#print TTMPERatio
#print PBRatio
#print PSRatio
#print HaltFlag

conn= MySQLdb.connect(
        host='192.168.31.215',
        port = 3306,
        user='root',
        passwd='jian182897',
        db ='SnowStock',
        )
cur = conn.cursor()

insert_sql="insert into snowdaily values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_param=(StockCode,StockName,Datekey,Timekey,HaltFlag,CurrentPrice,PriceChange,QuoteChange,YestClose,TodayOpen,TodayHigh,TodayLow,TodayRange,UpLimit,DownLimit,YearHigh,YearLow,Volume,Turnover,TotalValue,TotalCapital,FlowCapital,PerEarnings,PerDividend,PerNetAssets,LYRPERatio,TTMPERatio,PBRatio,PSRatio,Field1,Field2,Field3,CreatDate) 

cur.execute(insert_sql,sql_param)
cur.close()
conn.commit()
conn.close()

