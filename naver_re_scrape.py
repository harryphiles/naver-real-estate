# v0.5

from operator import itemgetter
import requests
import json
import logging

url = 'https://m.land.naver.com/complex/getComplexArticleList' #basic url

list = []

def get_info(tradTpCd, spc_min, spc_max, hscpNo):
    param = {
        'tradTpCd': tradTpCd, # A1: 매매, B1: 전세, B2: 월세
        'hscpNo': hscpNo, # building complex unique number
        'order': 'prc', # order of list (point_, date_, prc)
        'showR0': 'N',
    }

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'Referer': 'https://m.land.naver.com/'
    }

    logging.basicConfig(level=logging.INFO)
    page = 0

    while True:
        page += 1
        param['page'] = page

        r = requests.get(url, params=param, headers=header)
        if r.status_code != 200:
            logging.error('status code: %d' % r.status_code)
            break

        print_url = f'https://m.land.naver.com/complex/info/{hscpNo}?tradTpCd={tradTpCd}&ptpNo=&bildNo=&articleListYN=Y'

        load_json = json.loads(r.text)
        result = load_json['result']
        if result is None:
            logging.error('no result')
            break
        elif param['page'] == 1:
            print('{}'.format(result['list'][0]['atclNm'])) #, print_url)
            list.clear()
  
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

def get_list(): #--> new function to get list
    for i in list:
        if i[1] != i[2]:
            print('{} | {} | {} | {} | {}'.format(i[0], i[1], i[3], i[2], i[4]))
        else:
            print('{} | {} | {} |           | {}'.format(i[0], i[1], i[3], i[4]))

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
def search_individual():
    get_info('B1', 40, 130, 111059)
    get_list()

search_min(watch_list_1)
#search_list(watch_list_1)

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