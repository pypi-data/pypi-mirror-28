import urllib.request
import urllib.parse
import json
import os
import re


APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/zidian/word'

'''过滤HTML标记'''
def _strip_html_tags(tags):
    tags = tags.replace('<br />',os.linesep)
    tags = tags.replace('\u3000','')
    dr = re.compile('<[^>]+>',re.S)
    tags = dr.sub('',tags).strip()
    return tags

'''新华词典'''
def char_info(char=''):
    if len(char) != 1:
        return -1
    data = {}
    data['appkey'] = APPKEY
    data['word'] = char
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        for item in res['explain']:
            item['content'] = _strip_html_tags(item['content'])
        return res
    else:
        return -1


def main():
    print(char_info('好'))

if __name__ == '__main__':
    main()
