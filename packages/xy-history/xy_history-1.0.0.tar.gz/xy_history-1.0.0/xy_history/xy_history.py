import urllib.request
import urllib.parse
import json
import os
import arrow
import re


APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/todayhistory/query'

'''历史上的今天'''
def history_info(month='',day=''):
    data = {}
    data['appkey'] = APPKEY
    utcdate = arrow.utcnow().date()
    if not month:
        month = utcdate.month
    if not day:
        day = utcdate.day
    data['month'] = month
    data['day'] = day
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    res = jsonarr['result']
    if res:
        for item in res:
            item['content'] = item['content'].replace('<br />',os.linesep)
            item['content'] = item['content'].replace('&nbsp;','')
            item['content'] = item['content'].replace('&ldquo;','“')
            item['content'] = item['content'].replace('&rdquo;','”')
            dr = re.compile('<[^>]+>',re.S)
            item['content'] = dr.sub('',item['content']).strip()
        return res
    else:
        return -1

# {'title': '英格兰首次发行彩票', 'year': '1569', 'month': '1', 'day': '11', 'content': '<p>&nbsp;&nbsp;&nbsp;&nbsp; 1569年1月11日，英格兰首次发行彩票。</p>'}

def main():
    print(history_info())

if __name__ == '__main__':
    main()
