import urllib.request
import urllib.parse
import json


showapi_appid="53391"
showapi_sign="890894ac7b444ff4baea4583a559ae5d"

'''
正确返回结果，错误返回-1
'''
def soup_info(count=1):
    if count < 1:
        count = 1
    if count >10:
        count = 10
    url="http://route.showapi.com/1211-1"
    send_data = urllib.parse.urlencode([
    ('showapi_appid', showapi_appid),
    ('showapi_sign', showapi_sign),
    ('count',count)

    ])
    req = urllib.request.Request(url)
    try:
           response = urllib.request.urlopen(req, data=send_data.encode('utf-8'), timeout = 10) # 10秒超时反馈
    except Exception as e:
        print(e)
    result = response.read().decode('utf-8')
    result_json = json.loads(result)
    if result_json['showapi_res_body']['ret_code'] == 0:
        return result_json['showapi_res_body']['data']
    else:
        return -1


def main():
    print(soup_info(5))

if __name__ == '__main__':
    main()
