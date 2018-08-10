import sqlite3
import json
import codecs

conn = sqlite3.connect('TaipeiCase.sqlite')
cur = conn.cursor()

#asql = ('SELECT * FROM CASE_ISSUE where case_id = 1 and lat != 0')
asql = ('''SELECT * FROM CASE_ISSUE where case_id = 3 and stolen_date> '20150101' and lat != 0''')
fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("function getPoints() {\n")
fhand.write("    return [\n")

count = 0
for aRow in cur.execute(asql) :
    lat = aRow[6]
    lng = aRow[7]
    #if lat == 0.0 or lng == 0.0 : continue

    try :
        count = count + 1
        if count > 1 : fhand.write(",\n")      #這個是幫上一行加enter
        
        output = "        new google.maps.LatLng(" + str(lat) + ", " + str(lng) +")"
        #print(output)
        fhand.write(output)
    except:
        print('E')
        continue

fhand.write("\n    ];\n")
fhand.write("\n}\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")