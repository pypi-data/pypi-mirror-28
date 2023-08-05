import urllib.request
import urllib.parse
import json
import os
import re


APPKEY='631c5a5b9992bd74'
API_URL='http://api.jisuapi.com/iqa/query'
'''
根据问题返回答案
'''
def chat(question=''):
    if question == '':
        return -1
    data = {}
    data['appkey'] = APPKEY
    data['question']=question
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr= json.loads(result.read())
    res = jsonarr['result']
    res_info = {}
    if res['content']:
        res['content'] = res['content'].replace('<br>',os.linesep)
        res['content'] = res['content'].replace('</br>','')
        res['content'] = re.sub('(.*?)\[link .*\](.*?)\[/link\]',r'\1\2',res['content'])
        res_info['content'] = res['content']
        res['relquestion'] = res['relquestion'].replace('<br>',os.linesep)
        res['relquestion'] = res['relquestion'].replace('</br>','')
        res_info['relquestion'] = res['relquestion']
        return res_info
    else:
        return -1
