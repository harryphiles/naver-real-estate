# v0.5

from operator import itemgetter
import requests
import json
import logging
from telegram import sendTelegramMsg
from watch_list import *

url = 'https://m.land.naver.com/complex/getComplexArticleList' #base url

list = []
list_min = []
list_min_result = []

### core functions
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
            #list.append(result['list'][0]['atclNm'])
  
        for item in result['list']:
            if float(item['spc2']) >= spc_min and float(item['spc2']) < spc_max:
                atclNm = item['atclNm']
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
                x = [atclNm, spc2, prc, prc_min, flrInfo, desc]
                list.append(x)     

        if result['moreDataYn'] == 'N':
            break

def get_min(): #--> new function to get min
    s = sorted(list, key=itemgetter(3))
    spc = []
    for i in s:
        spc.append(i[1])
    spc_s = sorted(set(spc))
    for i in spc_s:
        print(i, s[spc.index(i)][3])

def get_list_min(): #--> new function to get min
    #list_min.clear()
    #list_min.append(list[0])
    #list.remove(list[0])
    s = sorted(list, key=itemgetter(3))
    spc = []
    for i in s:
        spc.append(i[1])
    spc_s = sorted(set(spc))
    for i in spc_s:
        list_min.append([i, s[spc.index(i)][3], s[spc.index(i)][0]])

def get_list(): #--> new function to get list
    for i in list:
        if i[2] != i[3]:
            print('{} | {} | {} | {} | {}'.format(i[1], i[3], i[2], i[4], i[5]))
        else:
            print('{} | {} | {} |           | {}'.format(i[1], i[2], i[4], i[5]))

### watch list search ###
def search_min(x):
    for i in x:                         # change number to show results of different lists
        get_info('B1', i[1], 85, i[0])  # 기본
        get_min()

def search_list(x):
    for i in x:                         # change number to show results of different lists
        get_info('B1', i[1], 85, i[0])  # 기본
        get_list()                      # 보기: 모든 매물

### indivisual search ###
def search_individual(x):
    get_info('B1', 40, 130, x)
    get_list()

def search_min_test(watch_list, prc_max):
    for i in watch_list:                         # change number to show results of different lists
        get_info('B1', i[1], 85, i[0])  # 기본
        get_list_min()
    for i in list_min:
        try:
            prc = int('{:.1}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
        except:
            prc = int('{:.1}0000'.format(i[1].split()[0]))
        if prc <= prc_max:
            list_min_result.append(i)
    x = ''
    for i in range(len(list_min_result)):
        x += list_min_result[i][0] + " | " + list_min_result[i][1] + " | " + list_min_result[i][2] + "\n"
    if len(list_min_result) > 0:
        print(x)
        sendTelegramMsg("1726140050", x) # 1726140050 # 2022415076
        sendTelegramMsg("2022415076", x) 


search_min_test(watch_list_8, 35000)
#sendMsgToHer('testing')

# get_info('B1', 40, 130, 107999)
# get_min()
# title = list[0]
# get_min_list()
# print(list_min)
# x = ''
# for i in range(len(list_min)):
#     if i == 0:
#         x += title + "\n"
#         x += list_min[i][0] + " " + list_min[i][1] + "\n"
#     else:
#         x += list_min[i][0] + " " + list_min[i][1] + "\n"
# sendMsgToMe(x)


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