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
list_test_unique = []
list_test_target = []

list_add_new = []
list_result = []

### core functional functions ###
def get_info(tradTpCd, spc_min, spc_max, hscpNo):
    param = {
        'tradTpCd': tradTpCd, # A1: 매매, B1: 전세, B2: 월세
        'hscpNo': hscpNo, # building complex unique number
        'order': 'prc', # order of list (point_, date_, prc)
        'showR0': 'N',
    }

    header = {
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        #'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
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

# sort list_test_add
def sort_list(prc_max):
    list_test_target.clear()
    s = sorted(list_test_add, key=itemgetter(3))
    for i in s:
        try:
            if i[3].find("억") == 1:
                prc = int('{:.1}{:.1}{}'.format(i[3].split()[0], i[3].split()[1], i[3].split(",")[1]))
            else:
                prc = int('{:.2}{:.1}{}'.format(i[3].split()[0], i[3].split()[1], i[3].split(",")[1]))
        except:
            if i[3].find("억") == 1:
                prc = int('{:.1}0000'.format(i[3].split()[0]))
            else:
                prc = int('{:.2}0000'.format(i[3].split()[0]))
        if prc <= prc_max:
            list_test_target.append(i)

def get_min(): #--> new function to get min
    s = sorted(list, key=itemgetter(3))
    spc = []
    for i in s:
        spc.append(i[1])
    spc_s = sorted(set(spc))
    for i in spc_s:
        print('{} | {} | {}'.format(i, s[spc.index(i)][3], s[spc.index(i)][0]))

def get_unique_test(): #--> new function to get min
    list = list_test_add
    setter = []
    for i in list:
        setter.append(hash(i[0])+hash(i[1]))
    sorted_setter = set(setter)
    for i in sorted_setter:
        list_test_unique.append([list[setter.index(i)][0], list[setter.index(i)][1], list[setter.index(i)][3]])

def get_list_min(): #--> new function to get min
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
            print('{:.6} | {} | {} | {} | {} | {}'.format(i[0], i[1], i[3], i[4], i[2], i[5]))
        else:
            print('{:.6} | {} | {} | {} |           | {}'.format(i[0], i[1], i[2], i[4], i[5]))

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

### 
def search_min_test(watch_list, prc_max): #-> testing purposes
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

# get_info -> list_test_add
def get_data(watch_list): #-> to list_test_add
    list_test_add.clear()

    print(time.strftime("%H:%M:%S"))

    # for i in range(int(len(watch_list))):
    for i in range(len(watch_list)):
        rand_num = random.uniform(0.5, 2)
        time.sleep(rand_num)
        print(watch_list[i])
        if i < 10:
            get_info('B1', watch_list[i][1], 85, watch_list[i][0])
            add_list()
        if i == 10:
            time.sleep(random.uniform(10, 12))
        if 10 <= i < 20:
            get_info('B1', watch_list[i][1], 85, watch_list[i][0])
            add_list()
        if i == 20:
            time.sleep(random.uniform(20, 30))
        if 20 <= i < 30:
            get_info('B1', watch_list[i][1], 85, watch_list[i][0])
            add_list()
    
    print(time.strftime("%H:%M:%S"))

### new core functional functions ###
def get_info_new(tradTpCd, spc_min, spc_max, hscpNo):
    list = []
    param = {
        'tradTpCd': tradTpCd, # A1: 매매, B1: 전세, B2: 월세
        'hscpNo': hscpNo, # building complex unique number
        'order': 'prc', # order of list (point_, date_, prc)
        'showR0': 'N',
    }

    header = {
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        #'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }

    page = 0

    while True:
        page += 1
        param['page'] = page

        r = requests.get(url, params=param, headers=header)
        if r.status_code != 200:
            #logging.error('status code: %d' % r.status_code)
            #sendTelegramMsg("1726140050", "Error!")
            sys.exit(0)

        load_json = json.loads(r.text)
        result = load_json['result']
        if result is None:
            #logging.error('no result')
            break
  
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

    list_add_new.append(list)

def get_data_new(watch_list): #-> to list_test_add
    #list_test_add.clear()
    for i in range(len(watch_list)):
        rand_num = random.uniform(0.5, 2)
        time.sleep(rand_num)
        print(watch_list[i])
        if i < 10:
            get_info_new('B1', watch_list[i][1], 85, watch_list[i][0])
        if i == 10:
            time.sleep(random.uniform(10, 12))
        if 10 <= i < 20:
            get_info_new('B1', watch_list[i][1], 85, watch_list[i][0])
        if i == 20:
            time.sleep(random.uniform(20, 30))
        if 20 <= i < 30:
            get_info_new('B1', watch_list[i][1], 85, watch_list[i][0])

def data_processing(list):
    ## only get values below condition
    list1 = []
    for i in list:
        list_temp = []
        for j in i:
            try:
                if j[3].find("억") == 1:
                    prc = int('{:.1}{:.1}{}'.format(j[3].split()[0], j[3].split()[1], j[3].split(",")[1]))
                else:
                    prc = int('{:.2}{:.1}{}'.format(j[3].split()[0], j[3].split()[1], j[3].split(",")[1]))
            except:
                if j[3].find("억") == 1:
                    prc = int('{:.1}0000'.format(j[3].split()[0]))
                else:
                    prc = int('{:.2}0000'.format(j[3].split()[0]))
            if prc <= 50000:
                list_temp.append(j)
        list1.append(list_temp)

    ## sort by minimum prc
    list2 = []
    for i in list1:
        s = sorted(i, key=itemgetter(3))
        list_temp = []
        for j in s:
            list_temp.append(j)
        list2.append(list_temp)

    ### minimum values for each spc for each complex
    # list3 = []
    for i in list2:
        s = sorted(i, key=itemgetter(1))
        list_temp = []
        for j in s:
            list_temp.append(j[1])
        set_s = sorted(set(list_temp))
        list_temp2 = []
        for k in set_s:
            list_temp2.append(s[list_temp.index(k)])
        list_result.append(list_temp2)


# with list -> send telegram msg
def send_msg_with_list():
    x = ''
    if len(list_test_target) > 0:
        for i in range(len(list_test_target)):
            x += list_test_target[i][1] + " | " + list_test_target[i][3] + " | " + list_test_target[i][0] + "\n"
        # print(x)
        sendTelegramMsg("1726140050", x)
        sendTelegramMsg("2022415076", x)
    else:
        sendTelegramMsg("1726140050", "No result")

def send_msg_with_list_new():
    x = ''
    if len(list_result) > 0:
        for i in list_result:
            for j in i:
                x += j[1] + " | " + j[3] + " | " + j[0] + "\n"
        sendTelegramMsg("1726140050", x)
        sendTelegramMsg("2022415076", x)
    else:
        sendTelegramMsg("1726140050", "No result")

### combined ###
def alert(watch_list, prc_max):
    get_data_new(watch_list)
    data_processing(list_add_new)
    send_msg_with_list_new()
# def alert(watch_list, prc_max):
#     get_data(watch_list)
#     sort_list(prc_max)
#     send_msg_with_list()





# search_min(watch_list_a)
# search_list(watch_list_1)
# search_individual()
# alert(watch_list_a, 35000)