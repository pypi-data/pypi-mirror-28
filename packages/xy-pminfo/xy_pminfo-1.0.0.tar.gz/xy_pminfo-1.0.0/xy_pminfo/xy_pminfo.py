import urllib.request
import urllib.parse
import json


APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/aqi/query'

'''谜语'''
def city_pm(city=''):
    if city == '':
        return -1
    data = {}
    data['appkey'] = APPKEY
    data['city'] = city
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        res_dict = {}
        res_dict['city']=res['city']
        res_dict['pm25']=res['pm2_524']
        res_dict['quality']=res['quality']
        res_dict['level']=res['aqiinfo']['level']
        res_dict['affect']=res['aqiinfo']['affect']
        res_dict['advise']=res['aqiinfo']['measure']
        return res_dict
    else:
        return -1


def main():
    print(city_pm('哈尔滨'))

if __name__ == '__main__':
    main()
