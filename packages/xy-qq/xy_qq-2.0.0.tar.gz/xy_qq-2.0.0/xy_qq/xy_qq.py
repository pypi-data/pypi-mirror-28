import urllib.request
import urllib.parse
import json
APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/qqluck/query'

'''qq号码测试'''
def luck(qq=''):
    if qq == '':
        return -1
    data = {}
    data['appkey'] = APPKEY
    data['qq'] = qq
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        res_dict = {}
        res_dict['qq']=res['qq']
        res_dict['luck']=res['luck']
        res_dict['socre']=res['score']
        res_dict['content']=res['content']
        res_dict['character']=res['character']
        res_dict['detail']=res['characterdetail']
        return res_dict
    else:
        return -1
