import urllib.request
import urllib.parse
import json


APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/aqi/city'

'''获取所有城市'''
def get_citys():
    data = {}
    data['appkey'] = APPKEY
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        return res
    else:
        return -1

def main():
    print(get_citys())

if __name__ == '__main__':
    main()
