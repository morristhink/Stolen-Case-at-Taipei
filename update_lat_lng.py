#測試時先call 一次google api成功就好, 整個寫好再全部查
import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = 'place your api key here'
serviceurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('TaipeiCase.sqlite')
cur = conn.cursor()
curUpd = conn.cursor()

def getGeo(aDict):
    aLat = 0.0
    aLng = 0.0
    url = serviceurl + urllib.parse.urlencode(aDict)
    #print(url)    
    
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    
    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        return aLat, aLng

    if not('status' in js and js['status'] == 'OK'): 
        return aLat, aLng
        
    aLat = js["results"][0]["geometry"]["location"]["lat"]
    aLng = js["results"][0]["geometry"]["location"]["lng"]
    #print(aLat, aLng)
    return aLat, aLng
    

#更新各區經緯度
aSql = 'SELECT id, title, Lat FROM DICT_INFO'
queryAddress = ''

for aRow in cur.execute(aSql):
    #print('台北巿' + aRow[1])
    
    if aRow[2] != 0.0:
        #print('1', aRow[2])
        continue
    #print('1', aRow[2])
    #break
    parms = dict()
    dictid = aRow[0]
    queryAddress = '台北巿' + aRow[1]
    parms["query"] = queryAddress
    
    if api_key is not False: parms['key'] = api_key

    lat, lng = getGeo(parms)
    #print('1',lat, lng)
    #break
    if lat == 0 or lng == 0:
        continue
        
    #print(queryAddress, lat, lng)    
    
    curUpd.execute('''update DICT_INFO set Lat = ?, Lng = ? 
                       where id = ?''', (lat, lng, dictid))
    conn.commit()

#更新案件經緯度
aSql = 'SELECT id, location, Lat FROM CASE_ISSUE where case_id = 3'
count = 0
for aRow in cur.execute(aSql):
    if aRow[2] != 0.0:
        #print('1', aRow[2])
        continue
    #print('1', aRow[2])
    #break
    parms = dict()
    caseid = aRow[0]
    queryAddress = aRow[1]
    parms['query'] = queryAddress
    
    if api_key is not False: parms['key'] = api_key

    lat, lng = getGeo(parms)
    #print(parms['query'],lat, lng)     #發現json裡有很多地址都是錯的
    #break
    if lat == 0 or lng == 0:
        continue
        
    #print(queryAddress, lat, lng)    
    
    curUpd.execute('''update CASE_ISSUE set Lat = ?, Lng = ? 
                       where id = ?''', (lat, lng, caseid))
    count += 1    
    if count % 20 == 0:
        conn.commit()

    conn.commit()
   
cur.close()