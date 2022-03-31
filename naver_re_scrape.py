# v0.3

import requests
import json
import logging

url = 'https://m.land.naver.com/complex/getComplexArticleList' #basic url

l_spc2 = []
l_prc = []
l_prc_min = []
l_desc = []
l_flrInfo = []
#title = []

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
            l_spc2.clear()
            l_prc.clear()
            l_prc_min.clear()
            l_desc.clear()
            l_flrInfo.clear()
                # title.clear()
                # title.append('{}'.format(result['list'][0]['atclNm']))

        for item in result['list']:
            spc2 = '{:.4}'.format(item['spc2'])
            prc = '{:8}'.format(item['prcInfo'])
            #prc_max = '{:8}'.format(item['sameAddrMaxPrc'])
            prc_min = '{:8}'.format(item['sameAddrMinPrc'])
            try:
                desc = item['atclFetrDesc']
            except:
                desc = 'none'
            if item['flrInfo'][:item['flrInfo'].find('/')].isnumeric():
                flrInfo = '{:>5}'.format(item['flrInfo'])
            else:
                flrInfo = '{:>4}'.format(item['flrInfo'])
            if float(item['spc2']) >= spc_min and float(item['spc2']) < spc_max:
                l_spc2.append(spc2)
                l_prc.append(prc)
                l_prc_min.append(prc_min)
                l_desc.append(desc)
                l_flrInfo.append(flrInfo)        

        if result['moreDataYn'] == 'N':
            break

def get_min():
    for i in sorted(set(l_spc2)):
        if l_prc[l_spc2.index(i)] != l_prc_min[l_spc2.index(i)]:
            print('{} | {}'.format(i, l_prc_min[l_spc2.index(i)]))
        else:
            print('{} | {}'.format(i, l_prc[l_spc2.index(i)]))

def get_list():
    for i in range(len(l_spc2)):
        if l_prc[i] != l_prc_min[i]:
            print('{} | {} | {} | {} | {}'.format(l_spc2[i], l_prc[i], l_flrInfo[i], l_prc_min[i], l_desc[i]))
        else:
            print('{} | {} | {} |           | {}'.format(l_spc2[i], l_prc[i], l_flrInfo[i], l_desc[i]))

### watch list
watch_list_1 = [
    [111059, 40], # 광교지웰홈스
    [103994, 45], # 에듀하임
    [114777, 50]  # 힐스테이트광교중앙역
]

watch_list_2 = [
    [102530, 40], # 수지_푸르지오월드마크(주상복합)
    [10244, 40],  # 정자_두산위브파빌리온
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

### watch list search
for i in watch_list_1:              # change number to show results of different lists
    get_info('B1', i[1], 85, i[0])  # 기본
    get_min()                       # 보기: 각 평수당 최소 보증금만
    get_list()                      # 보기: 모든 매물
    # print('\n')

### indivisual search
# get_info('B1', 40, 130, 114777)
# get_min()
# get_list()


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