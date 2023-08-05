import urllib.request
import urllib.parse
import json
import re

APPKEY='631c5a5b9992bd74'
API_URL='http://api.jisuapi.com/translate/translate'
'''英译汉'''
def en2zh(text=''):
    if text == '':
        return -1
    data = {}
    data["appkey"] = APPKEY
    data["type"] = "baidu"
    data["from"] = "en"
    data["to"] = "zh-cn"
    data["text"] = text

    url_values = urllib.parse.urlencode(data)
    url = API_URL + "?" + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res['result']:
        res['result'] = res['result'].replace('<br />','\n')
        dr = re.compile('<[^>]+>',re.S)
        res_str = dr.sub('',res['result']).strip()
        return res_str
    else:
        return -1

'''汉译英'''
def zh2en(text=''):
    if text == '':
        return -1
    data = {}
    data["appkey"] = APPKEY
    data["type"] = "baidu"
    data["from"] = "zh-cn"
    data["to"] = "en"
    data["text"] = text

    url_values = urllib.parse.urlencode(data)
    url = API_URL + "?" + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res['result']:
        res['result'] = res['result'].replace('<br />','\n')
        dr = re.compile('<[^>]+>',re.S)
        res_str = dr.sub('',res['result']).strip()
        return res_str
    else:
        return -1
