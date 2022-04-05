# v0.5

from operator import itemgetter
import requests
import json
import logging

url = 'https://m.land.naver.com/complex/getComplexArticleList' #basic url
KAKAO_TOKEN = "PwGTvue3aeqF3WY894pKvrYCEc8JFwlcsCgJGQo9dNoAAAF_-FQqYQ"

list = []
list_min = []

def get_info(tradTpCd, spc_min, spc_max, hscpNo):
    param = {
        'tradTpCd': tradTpCd, # A1: 매매, B1: 전세, B2: 월세
        'hscpNo': hscpNo, # building complex unique number
        'order': 'prc', # order of list (point_, date_, prc)
        'showR0': 'N',
    }

    header = {
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }

    page = 0

    while True:
        page += 1
        param['page'] = page

        r = requests.get(url, params=param, headers=header)
        if r.status_code != 200:
            logging.error('status code: %d' % r.status_code)
            break

        load_json = json.loads(r.text)
        result = load_json['result']
        if result is None:
            logging.error('no result')
            break
        elif param['page'] == 1:
            #print('{}'.format(result['list'][0]['atclNm'])) #, print_url)
            list.clear()
            list.append(result['list'][0]['atclNm'])
  
        for item in result['list']:
            if float(item['spc2']) >= spc_min and float(item['spc2']) < spc_max:
                spc2 = '{:.4}'.format(item['spc2'])
                prc = '{:8}'.format(item['prcInfo'])
                prc_min = '{:8}'.format(item['sameAddrMinPrc'])
                try:
                    desc = item['atclFetrDesc']
                except:
                    desc = 'none'
                if item['flrInfo'][:item['flrInfo'].find('/')].isnumeric():
                    flrInfo = '{:>5}'.format(item['flrInfo'])
                else:
                    flrInfo = '{:>4}'.format(item['flrInfo'])
                x = [spc2, prc, prc_min, flrInfo, desc]
                list.append(x)     

        if result['moreDataYn'] == 'N':
            break

def get_min(): #--> new function to get min
    s = sorted(list, key=itemgetter(2))
    spc = []
    for i in s:
        spc.append(i[0])
    spc_s = sorted(set(spc))
    for i in spc_s:
        print(i, s[spc.index(i)][2])

def get_min_list(): #--> new function to get min
    #list_min.clear()
    #list_min.append(list[0])
    list.remove(list[0])
    s = sorted(list, key=itemgetter(2))
    spc = []
    for i in s:
        spc.append(i[0])
    spc_s = sorted(set(spc))
    for i in spc_s:
        list_min.append([i, s[spc.index(i)][2]])

def get_list(): #--> new function to get list
    for i in list:
        if i[1] != i[2]:
            print('{} | {} | {} | {} | {}'.format(i[0], i[1], i[3], i[2], i[4]))
        else:
            print('{} | {} | {} |           | {}'.format(i[0], i[1], i[3], i[4]))

def sendMsgToMe(input): #--> new fn to send msg to kakaotalk
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}

    post = {
        "object_type": "text",
        "text": input,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        }
    }

    data = {"template_object": json.dumps(post)}
    
    return requests.post(url, headers=header, data=data)

### watch list
watch_list_1 = [
    [111059, 40],  # 광교지웰홈스
    [109829, 43],  # 광교_힐스테이트광교
    [103994, 45],  # 에듀하임
    [114777, 50]  # 힐스테이트광교중앙역
]
watch_list_2 = [
    [102530, 40],  # 수지_푸르지오월드마크(주상복합)
    [10244, 40],   # 정자_두산위브파빌리온
    [9896, 40]   # 구성_성호샤인힐즈
]
watch_list_3 = [
    [114593, 40],  # 광교_sk뷰레이크타워
    [111001, 40],  # 광교_중흥S-클래스
    [116449, 40]  # 광교_포레나광교
]
watch_list_4 = [
    [120682, 40],  # 광교_효성해링턴타워
    [120134, 40],  # 광교_효성해링턴타워레이크
    [107999, 43],  # 광교_더샵레이크파크
    [105468, 40]  # 광교_힐스테이트레이크
]
watch_list_5 = [  # southern 광교
    [120316, 40],  # 광교(남)_더샵광교레이크시티
    [110644, 40],  # 광교(남)_더샵
    [110643, 40]  # 광교(남)_아이파크
]
watch_list_6 = [  # 정자동
    [3014, 40],  # 느티마을공무원3단지 # 1994
    [2618, 40],  # 느티마을공무원4단지 # 1994
    [2645, 40]  # 상록우성 #1995
]
watch_list_7 = [  # 동탄역 동쪽
    [110527, 40],  # 동탄역린스트라우스(주상복합) # 2018
    [106031, 40],  # 동탄역시범한화꿈에그린프레스티지 # 2015
    [106558, 40],  # 동탄역시범더샵센트럴시티 # 2015
    [106155, 40],  # 동탄역시범한화꿈에그린프레스티지 # 2015
    [106031, 40],  # 동탄역시범대원칸타빌 # 2015
    [111024, 40],  # 동탄역시범금강펜테리움센트럴파크III # 2017
    [107542, 40],  # 동탄역시범예미지 # 2015
    [106154, 40],  # 동탄역시범리슈빌 # 2015
    [105405, 40],  # 동탄역시범우남퍼스트빌 # 2015
    [122159, 40],  # 동탄역예미지시그너스(주상복합) # 2021
    [110026, 40],  # 동탄역센트럴예미지 # 2017
    [105414, 40],  # 동탄센트럴자이 # 2015
    [119652, 40]  # 동탄역롯데캐슬(주상복합) # 2021
]
watch_list_8 = [  # 동탄역 서쪽
    [109931, 40],  # 반도유보라아이비파크5 # 2017
    [109932, 40],  # 반도유보라아이비파크6 # 2017
    [111352, 40],  # 반도유보라아이비파크8 # 2018
    [111351, 40],  # 반도유보라아이비파크7 # 2019
    [110140, 40],  # 동탄역푸르지오 # 2017
    [128133, 40],  # 동탄역유림노르웨이숲(주상복합) # 2021
    [116776, 40],  # 동원로얄듀크비스타3차(주상복합) # 2020
    [14371, 40],  # 동탄역신미주 # 2005
    [109947, 40]  # 동탄역에일린의뜰 # 2016
]

### watch list search ###
def search_min(x):
    for i in x:                         # change number to show results of different lists
        get_info('B1', i[1], 85, i[0])  # 기본
        get_min()                       # 보기: 각 평수당 최소 보증금만

def search_list(x):
    for i in x:                         # change number to show results of different lists
        get_info('B1', i[1], 85, i[0])  # 기본
        get_list()                      # 보기: 모든 매물

### indivisual search ###
def search_individual(x):
    get_info('B1', 40, 130, x)
    get_list()

### search min send text test
# def s(x):
#     for i in x:                         # change number to show results of different lists
#         get_info('B1', i[1], 85, i[0])  # 기본
#         get_min() 

get_info('B1', 40, 130, 120682)
title = list[0]
get_min_list()
print(list_min)
x = ''
for i in range(len(list_min)):
    if i == 0:
        x += title + "\n"
        x += list_min[i][0] + " " + list_min[i][1] + "\n"
    else:
        x += list_min[i][0] + " " + list_min[i][1] + "\n"
sendMsgToMe(x)


# search_min(watch_list_7)
# search_list(watch_list_5)
# search_individual(103994)

'''
# [120682, 40],  # 광교_효성해링턴타워
# [120134, 40],  # 광교_효성해링턴타워레이크
# [105468, 40],  # 광교_힐스테이트레이크
# [107999, 43],  # 광교_더샵레이크파크
# [109829, 43],  # 광교_힐스테이트광교
# [114777, 50],  # 힐스테이트광교중앙역
# [103994, 50],  # 에듀하임
# [114593, 40],  # 광교_sk뷰레이크타워
# [111001, 40],  # 광교_중흥S-클래스
# [116449, 40],  # 광교_포레나광교
# [110643, 40],  # 광교(남)_아이파크
# [120316, 40],  # 광교(남)_더샵광교레이크시티
# [110644, 40],  # 광교(남)_더샵
# [111059, 40],  # 광교지웰홈스
# [102530, 40],  # 수지_푸르지오월드마크(주상복합)
# [10244, 40],   # 정자_두산위브파빌리온
# [9896, 40]   # 구성_성호샤인힐즈
'''