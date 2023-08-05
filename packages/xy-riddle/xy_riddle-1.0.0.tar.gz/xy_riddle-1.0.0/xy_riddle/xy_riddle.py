import urllib.request
import urllib.parse
import json
import os
import random


APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/rkl/search'

'''谜语'''
def search(keyword=''):
    data = {}
    data['appkey'] = APPKEY
    data['pagesize'] = 1
    data['pagenum'] = 1
    data['classid'] = random.randint(1,11)
    data['keyword'] = keyword
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        res_dict = {}
        res_dict['title']=res['list'][0]['title']
        res_dict['content']=res['list'][0]['content'].replace('<br />',os.linesep)
        return res_dict
    else:
        return -1



def main():
    print(search())

if __name__ == '__main__':
    main()
