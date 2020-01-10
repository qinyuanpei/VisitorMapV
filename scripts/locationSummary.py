import leancloud
from collections import Counter
import json

# 初始化LeanCloud
leancloud.init("JbHqRp2eMrTgIwYpfERH0g79-gzGzoHsz", "VsiKvLuiBGvJL1XrAfv7siY2")

# 访客记录
VisitorRecord = leancloud.Object.extend('VisitorRecord')

# 位置汇总
LocationSummary = leancloud.Object.extend('LocationSummary')

# 查询地理信息
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

def save_locationSummary(obj):
    query = LocationSummary.query
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

geo_list = get_geoInfo(VisitorRecord.query)
latlng_list = list(map(lambda x:(x['latitude'],x['longitude']), geo_list))
print(Counter(latlng_list).items())
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
    save_locationSummary(location)
    