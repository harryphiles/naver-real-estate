# v0.5

from operator import itemgetter
from re import S
import requests
import json
import logging
import random
import time
import sys
from telegram import sendTelegramMsg
from watch_list import *

url = 'https://m.land.naver.com/complex/getComplexArticleList' #base url

list = []
list_min = []
list_min_result = []
list_test_add = [] # adding up lists made from get_info() fn
list_test_target = []

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
            sendTelegramMsg("1726140050", "Error!")
            sys.exit(0)

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
                # list_test_add.append(x)     

        if result['moreDataYn'] == 'N':
            break

def add_list():
    list_test_add.extend(list)

def sort_list(prc_max):
    s = sorted(list_test_add, key=itemgetter(3))
    for i in s:
        try:
            if i[1].find("억") == 1:
                prc = int('{:.1}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
            else:
                prc = int('{:.2}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
        except:
            if i[1].find("억") == 1:
                prc = int('{:.1}0000  '.format(i[1].split()[0]))
            else:
                prc = int('{:.2}0000  '.format(i[1].split()[0]))
        if prc <= prc_max:
            list_test_target.append(i)



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
            if i[1].find("억") == 1:
                prc = int('{:.1}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
            else:
                prc = int('{:.2}{:.1}{}'.format(i[1].split()[0], i[1].split()[1], i[1].split(",")[1]))
        except:
            if i[1].find("억") == 1:
                prc = int('{:.1}0000'.format(i[1].split()[0]))
            else:
                prc = int('{:.2}0000'.format(i[1].split()[0]))
        if prc <= prc_max:
            list_min_result.append(i)
    x = ''
    for i in range(len(list_min_result)):
        x += list_min_result[i][0] + " | " + list_min_result[i][1] + " | " + list_min_result[i][2] + "\n"
    if len(list_min_result) > 0:
        print(x)
        sendTelegramMsg("1726140050", x) # 1726140050 # 2022415076
        #sendTelegramMsg("2022415076", x) 

# for i in range(1, 3):
#     str = "watch_list_{}".format(i)
#     print(str[0])

def alert_system(prc_max):
    list_test_add.clear()
    list_test_target.clear()

    # for i in range(int(len(watch_list))):
    for i in range(0, 10):
        rand_num = random.uniform(1, 3)
        time.sleep(rand_num)
        print(watch_list[i])
        get_info('B1', watch_list[i][1], 85, watch_list[i][0])
        add_list()

    time.sleep(20)

    for i in range(10, 20):
        rand_num = random.uniform(1, 3)
        time.sleep(rand_num)
        print(watch_list[i])
        get_info('B1', watch_list[i][1], 85, watch_list[i][0])
        add_list()

    time.sleep(15)

    for i in range(20, 30):
        rand_num = random.uniform(1, 3)
        time.sleep(rand_num)
        print(watch_list[i])
        get_info('B1', watch_list[i][1], 85, watch_list[i][0])
        add_list()

    time.sleep(20)

    for i in range(30, 40):
        rand_num = random.uniform(1, 3)
        time.sleep(rand_num)
        print(watch_list[i])
        get_info('B1', watch_list[i][1], 85, watch_list[i][0])
        add_list()

    time.sleep(15)

    for i in range(40, 42):
        rand_num = random.uniform(1, 3)
        time.sleep(rand_num)
        print(watch_list[i])
        get_info('B1', watch_list[i][1], 85, watch_list[i][0])
        add_list()

    sort_list(prc_max)

    x = ''
    if len(list_test_target) > 0:
        for i in range(len(list_test_target)):
            x += list_test_target[i][0] + " | " + list_test_target[i][1] + " | " + list_test_target[i][3] + "\n"
        # print(x)
        sendTelegramMsg("1726140050", x)
    else:
        sendTelegramMsg("1726140050", "No result")

# print(list_test_target)

search_min_test(watch_list_3, 110000)