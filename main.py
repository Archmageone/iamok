
import execjs
import requests
import re
import json
import random

def sendmsgserver(url, title, content):
    mess = {
        "text": title,
        "desp": content
    }
    requests.post(url, data=mess)

def AutoKeepSafe(user, pw):                  # sign in scut and auto submit
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }
    Loginurl = 'https://sso.scut.edu.cn/cas/login?service=https%3A%2F%2Fiamok.scut.edu.cn%2Fcas%2Flogin'
    session = requests.Session()
    r = session.get(Loginurl, headers=headers1)
    lt = re.findall('id="lt" name="lt" value="(.*?)"', r.text)[0]
    execution = re.findall('name="execution" value="(.*?)"', r.text)[0]
    with open('des.js')as f:
        ctx = execjs.compile(f.read())
    s = user + pw + lt
    rsa = ctx.call('strEnc', user + pw + lt, '1', '2', '3')
    login_data = {
        'rsa': rsa,
        'ul': len(user),
        'pl': len(pw),
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit'
    }
    r = session.post(Loginurl, data=login_data, headers=headers1)
    getpath = 'https://iamok.scut.edu.cn/mobile/recordPerDay/getRecordPerDay'
    perdaydata = session.get(getpath, headers=headers1)
    a = perdaydata.json()
    datas = json.dumps(a['data'])
    print(datas)
    headers2 = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }
    SendstatementPath = 'https://iamok.scut.edu.cn/mobile/recordPerDay/submitRecordPerDay'
    r2 = session.post(SendstatementPath, data=datas, headers=headers2)
    datar2 = r2.json()
    state = datar2['msg']
    return state


# 校园账号密码
user = 'xxxxxxx'
pw = 'xxxxxxxx'
msg = AutoKeepSafe(user, pw)

RandNum = random.choice('abcdefghijklmnopqrstuvwxyz')
title = '今日报告:' + msg
content = """
# Markdown 
"""

# server酱url
serverurl = 'url'
sendmsgserver(serverurl, title, content+RandNum)
