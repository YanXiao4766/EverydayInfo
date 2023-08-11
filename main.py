import requests
import json
import os

url = ' http://bjb.yunwj.top/php/60miao/qq.php'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38"}

xia_token = os.environ.get('XIA_TOKEN')

def insert_line_breaks(original_string, num_chars):
    split_string = ""
    index = 0

    while index < len(original_string):
        split_string += original_string[index:index+num_chars] + "\n"
        index += num_chars

    return split_string

def getInfo():
    title = '60秒读懂世界'
    text=''
    data =[]
    
    res = requests.get(url,headers=headers).text
    js_text = json.loads(res)['wb']
    for i in range(len(js_text)):
        string = insert_line_breaks(js_text[i][0],23)
        data.append(string)
    text = '\n'.join(data)

    return {
        'text':title,
        'desp':text
    }


def main():
    data = getInfo()
    requests.post('http://wx.xtuis.cn/' + xia_token +'.send', data=data)

main()
