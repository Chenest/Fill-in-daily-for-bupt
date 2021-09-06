import requests
from config import *

DATA = {
    "ismoved": "0",  # 当前地点是否与上次在同一城市
    "jhfjrq": "",  # 计划返京时间
    "jhfjjtgj": "",  # 计划返京交通工具
    "jhfjhbcc": "",  # 计划返京航班班次/车次
    "sfxk": "0",  # 未解释
    "xkqq": "",  # 未解释
    "szgj": "",  # 所在国家
    "szcs": "",  # 所在地区
    "zgfxdq": "0",  # 中高风险地区
    "mjry": "0",  # 密切接触人员
    "csmjry": "0",  # 近14日内本人/共同居住者是否去过疫情发生场所
    "ymjzxgqk": "已接种两针",
    "xwxgymjzqk": "3",
    "tw": "2",  # 体温范围
    "sfcxtz": "0",  # 今日是否出现发热，咽痛，干咳，咳痰，乏力，呕吐，腹泻，嗅觉异常，味觉异常
    "sfjcbh": "0",  # 今日是否接触无症状感染/疑似/确诊人群
    "sfcxzysx": "0",  # 是否有任何与疫情相关的， 值得注意的情况
    "qksm": "",  # 情况说明
    "sfyyjc": "0",  # 是否到相关医院或门诊检查
    "jcjgqr": "0",  # 属于正常情况
    "remark": "",  # 其他信息
    "address": "北京市海淀区北太平庄街道北京邮电大学北京邮电大学海淀校区",
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":39.964128146702,\"R\":116.35913492838597,\"lng\":116.359135,\"lat\":39.964128},\"location_type\":\"html5\",\"message\":\"Get+ipLocation+failed.Get+geolocation+success.Convert+Success.Get+address+success.\",\"accuracy\":55,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"010\",\"adcode\":\"110108\",\"businessAreas\":[{\"name\":\"小西天\",\"id\":\"110108\",\"location\":{\"Q\":39.957147,\"R\":116.364058,\"lng\":116.364058,\"lat\":39.957147}},{\"name\":\"北下关\",\"id\":\"110108\",\"location\":{\"Q\":39.955976,\"R\":116.33873,\"lng\":116.33873,\"lat\":39.955976}},{\"name\":\"西直门\",\"id\":\"110102\",\"location\":{\"Q\":39.942856,\"R\":116.34666099999998,\"lng\":116.346661,\"lat\":39.942856}}],\"neighborhoodType\":\"科教文化服务;学校;高等院校\",\"neighborhood\":\"北京邮电大学\",\"building\":\"北京邮电大学国家大学科技园\",\"buildingType\":\"商务住宅;楼宇;商务写字楼\",\"street\":\"师大北路\",\"streetNumber\":\"19号\",\"country\":\"中国\",\"province\":\"北京市\",\"city\":\"\",\"district\":\"海淀区\",\"township\":\"北太平庄街道\"},\"formattedAddress\":\"北京市海淀区北太平庄街道北京邮电大学国家大学科技园北京邮电大学海淀校区\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "北京市++海淀区",
    "province": "北京市",
    "city": "北京市",
    "sfzx": "1",  # 是否在校
    "sfjcwhry": "0",  # 是否接触武汉人员
    "sfjchbry": "0",  # 今日是否接触过近14日内在湖北其他地区（除武汉）活动过的人员
    "sfcyglq": "0",  # 是否处于观察期
    "gllx": "",  # 观察场所
    "glksrq": "",  # 观测开始实际
    "jcbhlx": "",  # 接触人群类型
    "jcbhrq": "",  # 接触时间
    "bztcyy": "",  # 不合前一天同城原因
    "sftjhb": "0",  # 今日是否到过或者经停湖北其他地区(除武汉)
    "sftjwh": "0",  # 今日是否经停武汉
    "sfsfbh": "0",
    "xjzd": "",
    "jcwhryfs": "",
    "jchbryfs": "",
    "szsqsfybl": "0",
    "sfygtjzzfj": "",
    "gtjzzfjsj": "",
    "gtjzzchdfh": "",
    "fjqszgjdq": "",
    "sfjzxgym": "1",
    "sfjzdezxgym": "1",
    "jcjg": ""  # 未解释
}

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"


def login(user, sess):
    url = 'https://app.bupt.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.bupt.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex'
    headers = {
        'user-agent': agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'host': 'app.bupt.edu.cn',
        'cookie': 'eai-sess=rvf9fr5e62t9aidg36u17vbas3'
    }
    page1 = sess.get(url, headers=headers)

    url = 'https://app.bupt.edu.cn/uc/wap/login/check'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': 'eai-sess=rvf9fr5e62t9aidg36u17vbas3',
        'host': 'app.bupt.edu.cn',
        'origin': 'https://app.bupt.edu.cn',
        'referer': 'https://app.bupt.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.bupt.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex',
        'user-agent': agent
    }
    data = {
        'username': user['username'],
        'password': user['password']
    }
    page2 = sess.post(url, headers=headers, data=data)
    cookie = page2.headers['set-cookie']
    x = cookie.find(';')
    cookie = cookie[:x + 1]
    cookie = 'eai-sess=rvf9fr5e62t9aidg36u17vbas3;' + cookie
    return cookie


def index(sess, cookie):
    url = 'https://app.bupt.edu.cn/ncov/wap/default/index'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'host': 'app.bupt.edu.cn',
        'referer': 'https://app.bupt.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.bupt.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex',
        'user-agent': agent,
        'cookie': cookie
    }
    page3 = sess.get(url, headers=headers)


def post(sess, cookie):
    url = 'https://app.bupt.edu.cn/ncov/wap/default/save'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': cookie,
        'host': 'app.bupt.edu.cn',
        'origin': 'https://app.bupt.edu.cn',
        'referer': 'https://app.bupt.edu.cn/ncov/wap/default/index',
        'user-agent': agent
    }
    page4 = sess.get(url, headers=headers, data=DATA)


def main():
    for user in users:
        sess = requests.session()
        cookie = login(user, sess)
        index(sess, cookie)
        post(sess, cookie)


main()
