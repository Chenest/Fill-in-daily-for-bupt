#-*-coding=utf-8-*-
#encode=utf-8
import requests
from http import cookiejar
from bs4 import BeautifulSoup as bs
import datetime
from config import *

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"

def getLt(str):
    lt=bs(str,'html.parser')
    dic={}
    for inp in lt.form.find_all('input'):
        if(inp.get('name'))!=None:
            dic[inp.get('name')]=inp.get('value')
    return dic


def get_cookie(temp1,temp2):
    x1 = temp1.find('vt=')
    x2 = temp1.find(';', x1)
    vt = temp1[x1:x2]
    x1 = temp1.find('vjuid=')
    x2 = temp1.find(';', x1)
    vjuid = temp1[x1:x2 + 1]
    x1 = temp1.find('vjvd=')
    x2 = temp1.find(';', x1)
    vjvd = temp1[x1:x2 + 1]
    cookie = temp2[:-16] + vjuid + vjvd + vt
    return cookie

def get_counsellor_info(sess, name, cookie):
    url = 'https://service.bupt.edu.cn/site/user/form-search-user'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Cookie': cookie,
        'Host': 'service.bupt.edu.cn',
        'Origin': 'https://service.bupt.edu.cn',
        'Referer': 'https: // service.bupt.edu.cn / v2 / matter / start?id = 578',
        'Agent': agent
    }
    data = {
        'param': '{"keyword":"' + name + '","search_field":["name","number"],"depart_id":[],"job_id":[],"tag_id":[200076,195971,195969],"uids":[],"relation":[]}',
        'agent_uid': "",
        'starter_depart_id': "181841",
        'test_uid': "0"
    }
    page = sess.post(url, data=data, headers=headers, allow_redirects=False)
    text = page.text
    x1 = text.find('id')
    x1 = text.find(':', x1)
    id = text[x1+1:x1+6]
    x2 = text.find('number')
    x2 = text.find(':', x2)
    number = text[x2+1:x2+13]
    return id, number

def login(user):
    now = str(datetime.datetime.now())[0:10]
    header = {
        'User-Agent': agent
    }
    # setting cookie
    session = requests.Session()
    session.cookies = cookiejar.CookieJar()
    r = session.get('https://auth.bupt.edu.cn/authserver/login?service=https%3A%2F%2Fservice.bupt.edu.cn%2Fsite%2Flogin%2Fcas-login%3Fredirect_url%3Dhttps%253A%252F%252Fservice.bupt.edu.cn%252Fv2%252Fmatter%252Fstart%253Fid%253D578',
              headers=header)
    dic = getLt(r.text)

    post_URL = 'https://auth.bupt.edu.cn/authserver/login?service=https%3A%2F%2Fservice.bupt.edu.cn%2Fsite%2Flogin%2Fcas-login%3Fredirect_url%3Dhttps%253A%252F%252Fservice.bupt.edu.cn%252Fv2%252Fmatter%252Fstart%253Fid%253D578'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Host": "auth.bupt.edu.cn",
        "User-Agent": agent,
        "Referer": "https://auth.bupt.edu.cn/authserver/login?service=https://service.bupt.edu.cn/site/login/cas-login?redirect_url=https%3A%2F%2Fservice.bupt.edu.cn%2Fv2%2Fsite%2Findex",
        "Origin": "https: // auth.bupt.edu.cn"
    }

    data = {
        'username': user['username'],  # 此处为你的学号
        'password': user['password'],  # 你的密码
        'lt': dic['lt'],
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': '1'
    }
    page1 = session.post(post_URL, data=data, headers=headers, allow_redirects=False)
    if (page1.status_code == 200):
        raise ValueError("用户名或密码 错误")

    new_url = page1.headers['location']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": agent,
        "Referer": "https://auth.bupt.edu.cn/",
    }
    page2 = session.get(new_url, headers=headers, allow_redirects=False)
    new_url = page2.headers['location']
    headers['Cookie'] = page2.headers['set-cookie']
    page3 = session.get(new_url, headers=headers, allow_redirects=False)

    new_url = page3.headers['location']
    headers['Cookie'] = page3.headers['set-cookie']
    page4 = session.get(new_url, headers=headers, allow_redirects=False)

    headers = {'Accept': 'application/json, text/plain, */*', 'Origin': 'https://service.bupt.edu.cn',
               'Referer': 'https://service.bupt.edu.cn/v2/matter/start?id=578', "User-Agent": agent,
               'Host': 'service.bupt.edu.cn'}
    cookie = get_cookie(page3.headers['set-cookie'], page2.headers['set-cookie'])

    uid, number = get_counsellor_info(session, user['counsellor'], cookie)

    headers['Cookie'] = cookie
    new_url = 'https://service.bupt.edu.cn/site/apps/launch'
    data = {
        'data': '{"app_id":"578","node_id":"","form_data":{"1716":{"User_5":"' + user['name'] + '","User_7":"' + user['username'] + '","User_9":"信息与通信工程学院","User_11":"' + user['phone'] + '","Alert_65":"","Alert_67":"","Count_74":{"type":0,"value":1},"Input_28":"' + user['direction'] + '","Radio_52":{"value":"1","name":"本人已阅读并承诺"},"Radio_73":{"value":"1","name":"是"},"Calendar_47":"' + now + 'T02:28:39.000Z","Calendar_50":"' + now + 'T02:28:38.000Z","Calendar_62":"' + now + 'T00:00:00+08:00","Calendar_69":"' + now + 'T00:00:00+08:00","SelectV2_58":[{"name":"' + user['campus'] + '","value":"2","default":0,"imgdata":""}],"Validate_63":"","Validate_66":"","MultiInput_30":"' + user['reason'] + '","UserSearch_60":{"uid":' + uid + ',"name":"' + user['counsellor'] + '","number":' + number + '}}},"userview":1}',
        'starter_depart_id': '181841',
        'agent_uid': '',
        'test_uid': '0'
    }
    response = session.post(new_url, headers=headers, data=data)

for user in users:
    login(user)



