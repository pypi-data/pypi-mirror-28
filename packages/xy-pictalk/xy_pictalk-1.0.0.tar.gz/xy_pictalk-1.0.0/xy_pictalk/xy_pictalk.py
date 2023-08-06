import requests
import json
import os
import base64

API_URL = 'https://www.phpfamily.org/pictalk.php'

'''看图说话'''
def pic_talk(filename=''):
    if not filename:
        return -1
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img']=b64img
    r = requests.post(API_URL, data=data)
    res = r.json()
    if res['ret'] == 0:
        return res['data']['text']
    else:
        return -1

def main():
    res = pic_talk('1.jpg')
    print(res)

if __name__ == '__main__':
    main()
