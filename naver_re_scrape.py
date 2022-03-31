### v0.2

import requests
import json
import logging

url = 'https://m.land.naver.com/complex/getComplexArticleList' #basic url

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

        load_json = json.loads(r.text)
        result = load_json['result']
        if result is None:
            logging.error('no result')
            break
        elif param['page'] == 1:
            print('{}'.format(result['list'][0]['atclNm']))

        # print(r.url)
        # for item in result['list']:
        #     #logging.info('%s' % (item['atclNm']))
        #     if float(item['spc2']) < 49 or float(item['spc2']) > 85:
        #         continue
        #     #logging.info('%s %s %s' % (item['spc2'], item['prcInfo'], item['flrInfo'])) # item['atclFetrDesc']
        #     logging.info('{:.4}m2 {:8} {}'.format(item['spc2'], item['prcInfo'], item['flrInfo']))

        for item in result['list']:
            spc2 = '{:.4}m2'.format(item['spc2'])
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
                if prc != prc_min:
                    print('{} | {} | {} | {} | {}'.format(spc2, prc, flrInfo, prc_min, desc))
                else:
                    print('{} | {} | {} |           | {}'.format(spc2, prc, flrInfo, desc))

        if result['moreDataYn'] == 'N':
            break

### watch list search
# watch_list_primary = [
#     111059, # 광교지웰홈스
#     103994, # 에듀하임
#     114777  # 힐스테이트광교중앙역
# ]

# for i in watch_list_primary:
#     get_info('B1', i)

## indivisual search
get_info('B1', 40, 85, 111001)

# 120134 # 광교효성해링턴타워레이크
# 120682 # 광교효성해링턴타워
# 105468 # 광교힐스테이트레이크
# 107999 # 광교더샵레이크파크
# 109829 # 힐스테이트광교
# 114777 # 힐스테이트광교중앙역
# 103994 # 에듀하임
# 114593 # 광교sk뷰레이크타워
# 111001 # 중흥S-클래스
# 116449 # 포레나광교
# 110643 # 광교아이파크
# 120316 # 더샵광교레이크시티
# 110644 # 광교더샵
# 111059 # 광교지웰홈스