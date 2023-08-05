import urllib.request
import urllib.parse
import json
APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/xiaohua'

'''文字笑话'''
def text_jokes(pagesize=1,sort='rand'):
    if not isinstance(pagesize,int):
        return -1
    if pagesize < 1:
        pagesize = 1
    if pagesize > 20:
        pagesize = 20
    data = {}
    data['appkey'] = APPKEY
    data['pagesize'] = pagesize
    data['sort'] = sort
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '/text?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        for item in res['list']:
            del item['addtime']
            del item['url']
        return res['list']
    else:
        return -1

'''图片笑话'''
def pic_jokes(pagesize=1,sort='rand'):
    if not isinstance(pagesize,int):
        return -1
    if pagesize < 1:
        pagesize = 1
    if pagesize > 20:
        pagesize = 20
    data = {}
    data['appkey'] = APPKEY
    data['pagesize'] = pagesize
    data['sort'] = sort
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '/pic?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        for item in res['list']:
            del item['addtime']
            del item['url']
        return res['list']
    else:
        return -1

def main():
    # print(text_jokes(8))
    print(pic_jokes(8))

if __name__ == '__main__':
    main()
