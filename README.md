# Stolen-Case-at-Taipei
Because I live in Taipei and the Taipei City gov. had some open data, so i chosse the 
    - Stolen Car Case
    - Stolen House Case
    - Stolen Bike Case

They provide this data(1989-02-10 ~ 2018-06-30) in two different way: 
    CSV or API
you can search at http://data.taipei/opendata

such as car:
1. download the csv: http://data.taipei/opendata/datalist/datasetMeta?oid=9717c017-f17c-4610-b6fe-e92181381538

2. Api: http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=5928460b-ee8d-4323-b6ac-ad975dbb84c3 

And I write this small system by follow flow:

1. get the data from api parsing the JSON and insert in to the database (import_data.py, import_data_have_table.py)
2. use the google api to get those location (update_lat_lng.py)
3. use the location and gen where.js that use by testHeatMap.html, 
   telling which dict. of Taipei City is the most stolen case happen (make_js.py)

To create windows UI or dynamic html code is not my purpose, 
i want to write some query condition setting at the code and let people to set what the want to see

remark:
-- House case
http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=34a4a431-f04d-474a-8e72-8d3f586db3df
-- Sample data
{"_id":"4","編號":"4","案類":"住宅竊盜","發生(現)日期":"990407","發生時段":"04~06","發生(現)地點":"台北市萬華區雙園街61 ~ 90號"}

-- Car case
http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=5928460b-ee8d-4323-b6ac-ad975dbb84c3
-- Sample data
{"_id":"5","編號":"5","案類":"汽車竊盜","發生(現)日期":"1040121","發生時段":"04~06","發生(現)地點":"台北市中山區建國北路二段91~120號"}

- Bike case
http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=08052aba-d76d-4b25-93f7-e19cec685f5a
-- Sample data
{"_id":"1","編號":"1","案類":"自行車竊盜","發生(現)日期":"1020630","發生時段":"13~15","發生(現)地點":"台北市松山區三民路151 ~ 180號"}
