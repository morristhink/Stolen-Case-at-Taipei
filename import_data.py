import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys
import datetime

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('TaipeiCase.sqlite')
cur = conn.cursor()

# 目前測試階段先清空資料庫
# 之後應該要研究, 在回傳一堆重複資料時, 如何只insert新資料
cur.executescript('''
DROP TABLE IF EXISTS CASE_ISSUE;
DROP TABLE IF EXISTS CASE_INFO;
DROP TABLE IF EXISTS TIME_INFO;
DROP TABLE IF EXISTS DICT_INFO;

CREATE TABLE IF NOT EXISTS CASE_ISSUE (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    case_id         INTEGER,
    stolen_date     TEXT,
    time_id         INTEGER,
    dict_id         INTEGER,
    location        TEXT,
    Lat             REAL,
    Lng             REAL
);

CREATE TABLE CASE_INFO (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    desc    TEXT UNIQUE
);

CREATE TABLE TIME_INFO (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    zone    TEXT UNIQUE
);

CREATE TABLE DICT_INFO (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title       TEXT UNIQUE,
    Lat         REAL,
    Lng         REAL    
);

''')

#call taipei city gov. api - 汽車
url = 'http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=5928460b-ee8d-4323-b6ac-ad975dbb84c3'
print('Retrieving', url)

uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode("utf-8")

#parsing json
info = None
result_info = list()

try:
    info = json.loads(data)
except:
    print(data)  # We print in case unicode causes an error

result_info = info["result"]["results"]      #又是一個dictionary

if len(result_info) < 1:
    print('無資料')
    quit()

timeDict = dict()  
dictDict = dict()
caseInfo1st = True    
count = 0
caseId = 0      #for 讀取 CASE_INFO 的 ID
timeId = 0      #for 讀取 TIME_INFO 的 ID
dictId = 0      #for 讀取 DICT_INFO 的 ID

for aCase in result_info:    #一筆筆拆解
    id = aCase['_id']
    caseType = aCase['案類']
    caseDate = aCase['發生(現)日期']
    caseDate = 19110000 + int(caseDate)
    caseTime = aCase['發生時段']
    caseLocation = aCase['發生(現)地點']
    dictName = caseLocation[3:6]
    if caseLocation[:3] != '台北市':       #裡面資料有台北縣, 台中巿 @.@
        continue
    
    if caseLocation.find('號') > 0:
        #由於資料都會有 XX ~ XX號, 這樣在Google沒辦法查經緯度
        #所以都用第一個號碼為標的
        caseLocation = caseLocation[:caseLocation.find('~')] + '號'
    #print(id, caseType, caseDate, caseTime, caseLocation, dictName)
    #quit()

#insert case table and call google map api at update_lat_lng.py

#insert case_info once
    if caseInfo1st == True:
        cur.execute('''INSERT OR IGNORE INTO CASE_INFO (desc) 
            VALUES ( ? )''', ( caseType, ) )
        cur.execute('SELECT id FROM CASE_INFO WHERE desc = ? ', (caseType, ))
        caseId = cur.fetchone()[0]
        caseInfo1st = False
    
#insert time_info     
    if timeDict.get(caseTime, -1) == -1:
        cur.execute('''INSERT OR IGNORE INTO TIME_INFO (zone) 
            VALUES ( ?)''', ( caseTime, ) )
        cur.execute('SELECT id FROM TIME_INFO WHERE zone = ? ', (caseTime, ))
        timeId = cur.fetchone()[0]
        timeDict[caseTime] = timeId
        #print(timeDict.get(caseTime, -1))

#insert dict_info and call google map api to get lat, lng at update_lat_lng.py    
    if dictDict.get(dictName, -1) == -1:
        cur.execute('''INSERT OR IGNORE INTO DICT_INFO (title, Lat, Lng) 
            VALUES ( ?, ?, ?)''', ( dictName,0, 0, ) )
        cur.execute('SELECT id FROM DICT_INFO WHERE title = ? ', (dictName, ))
        dictId = cur.fetchone()[0] 
        dictDict[dictName] = dictId

    cur.execute('''INSERT OR IGNORE INTO CASE_ISSUE
        (case_id, stolen_date, time_id, dict_id, location, Lat, Lng) 
        VALUES ( ?, ?, ?, ?, ?, ?, ? )''', 
        ( caseId, str(caseDate), timeDict[caseTime], dictDict[dictName], caseLocation, 0, 0, ) )

    count += 1

    if count % 20 == 0:
        conn.commit()
        
    conn.commit()









