import leancloud
from collections import Counter
import requests
import sys
import json

VisitorRecord = leancloud.Object.extend('VisitorRecord')
LocationSummary = leancloud.Object.extend('LocationSummary')
session = requests.session()

def get_geoInfo(query): 
    geoInfo = []
    count = 0
    total = query.count()
    while count < total: 
        query.limit(1000)
        query.skip(count)
        query_list = query.find()
        count += len(query_list)
        geo_list = list(map(lambda x:x.get('visitor_geo'), query_list))
        geoInfo.extend(geo_list)
    return geoInfo

def get_regeo(obj, apiKey):
    url = 'http://restapi.amap.com/v3/geocode/regeo?key={apiKey}&location={lng},{lat}'.format(apiKey=apiKey, lng=obj.get('longitude'), lat=obj.get('latitude'))
    res = session.get(url)
    data = json.loads(res.text)
    print(data)
    if data['status'] == '1':
        if(type(data['regeocode']['addressComponent']['district']) == type('')):
            obj.set('region',data['regeocode']['addressComponent']['district'])
        if(type(data['regeocode']['addressComponent']['city']) == type('')):
            obj.set('city',data['regeocode']['addressComponent']['city'])
        if(type(data['regeocode']['addressComponent']['country']) == type('')):
            obj.set('country',data['regeocode']['addressComponent']['country'])
    return obj

def save_locationSummary(obj, apiKey):
    query = LocationSummary.query
    obj = get_regeo(obj, apiKey)
    query.equal_to('latitude',obj.get('latitude'))
    query.equal_to('longitude', obj.get('longitude'))
    query_list = query.find()
    if(len(query_list)> 0):
        result = query_list[0]
        result.set('total_pv',obj.get('total_pv'))
        result.set('total_uv',obj.get('total_uv'))
        result.set('city',obj.get('city'))
        result.set('region',obj.get('region'))
        result.set('country',obj.get('country'))
        result.save()
    else: 
        obj.save()

def run(appId, appKey, apiKey):
    leancloud.init(appId, appKey)
    geo_list = get_geoInfo(VisitorRecord.query)
    print(geo_list)
    latlng_list = list(map(lambda x:(x['latitude'],x['longitude']), geo_list))
    for group in Counter(latlng_list).items():
        location = LocationSummary()
        lat = group[0][0]
        lng = group[0][1]
        location.set('latitude',lat)
        location.set('longitude',lng)
        location.set('total_pv',group[1])
        geoInfos = list(filter(lambda x:x['latitude'] == lat and x['longitude'] == lng, geo_list))
        geoInfo = geoInfos[0] 
        geoUsers = list(map(lambda x:x['ip'], geoInfos))
        location.set('total_uv',len(Counter(geoUsers).items()))
        location.set('city',geoInfo.get('city',''))
        location.set('region',geoInfo.get('region',''))
        location.set('country',geoInfo.get('country'))
        save_locationSummary(location,apiKey)

if (__name__ == '__main__'):
    print(sys.argv[1] + ',' + sys.argv[2] + ',' + sys.argv[3])
    run(sys.argv[1],sys.argv[2],sys.argv[3])
    