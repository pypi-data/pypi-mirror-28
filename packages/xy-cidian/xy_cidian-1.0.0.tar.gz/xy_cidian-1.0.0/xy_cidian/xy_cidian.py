import urllib.request
import urllib.parse
import json
import os
import re


APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/cidian/word'

'''过滤HTML标记'''
def _strip_html_tags(tags):
    tags = tags.replace('<br />',os.linesep)
    dr = re.compile('<[^>]+>',re.S)
    tags = dr.sub('',tags).strip()
    return tags

'''汉语词典'''
def word_info(word=''):
    if word == '':
        return -1
    data = {}
    data['appkey'] = APPKEY
    data['word'] = word
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        for k,v in res.items():
            res[k] = _strip_html_tags(v)
        del res['comefrom']
        return res
    else:
        return -1


def main():
    print(word_info('中心'))

if __name__ == '__main__':
    main()
