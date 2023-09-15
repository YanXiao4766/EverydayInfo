import requests
import sys
from bs4 import BeautifulSoup

arguments = sys.argv
userName = arguments[1]
passWord = arguments[2]
xia_token = arguments[3]

url = 'https://www.sayhuahuo.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LUtj7&inajax=1'
checkPageUrl = 'https://www.sayhuahuo.net/dsu_paulsign-sign.html'
checkUrl = 'https://www.sayhuahuo.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38"}
checkHeader ={
        'Content-Type': 'application/x-www-form-urlencoded',
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38"}
session = requests.session()
  
  
def check():
    data = {
        'formhash' : '82e021cb',
        'referer' : 'https://www.sayhuahuo.net/home.php?mod=space&uid=124526',
        'username' : userName,
        'password': passWord,
        'questionid' : '0',
        'answer' :''
    }
    try:
        session.post(headers=headers,data=data,url=url)
    except Exception :
        return '登录失败'
    print('login')
    try:
        res = session.get(headers=headers,url=checkPageUrl)
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(res.text, "html.parser")
        formhash_tags = soup.find_all(attrs={"name": "formhash"})[0]
        formhash = formhash_tags['value']
    except Exception :
        return '获取formhash失败'
    if len(formhash) < 1:
        return '获取formhash失败'
    checkData = {'formhash' : formhash,'qdxq' : 'yl','qdmode' : '1','todaysay':'签到打卡','fastreply' : '0'}
    print('getFOrmHash: ' + formhash )
    try:
        res = session.post(headers=checkHeader,data=checkData,url=checkUrl)
        print(res.text)
        if '签到成功' in res.text:
            return '签到成功~'
        if '已经签到' in res.text:
            return '今天已经签到过了~'
    except Exception :
        return '签到失败！'
    
    return 'over'
    

def main():
    returnMsg = check()
    print(returnMsg)
    data = {
        'text':'Say花火签到提醒',
        'desp':returnMsg
    }
    requests.post('http://wx.xtuis.cn/' + xia_token +'.send', data=data)

main()
