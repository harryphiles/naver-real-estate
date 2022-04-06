KAKAO_TOKEN = "i-S98ui_X4NeGEfXambQ2Eeezg6Hvn6nMJ7EUgo9dGkAAAF__EbcGg"

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
    
    response = requests.post(url, headers=header, data=data)

    print(response.text)

def sendMsgToHer(input): #--> new fn to send msg to kakaotalk
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" #--> 친구에게 보내기 주소
    uuid = ["EyEXLxwlFiQQPA01BjMFNQI0BCgfLRoqGixh"]
    uuids = {"receiver_uuids": json.dumps(uuid)}
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}

    post = {
        "object_type": "text",
        "text": input,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
    }

    data = {"template_object": json.dumps(post)}
    uuids.update(data)

    response = requests.post(url, headers=header, data=uuids)

    print(response.text)


url = "https://kauth.kakao.com/oauth/token"

# data = {
#     "grant_type" : "authorization_code",
#     "client_id" : "4978360da1e4f3d72f005c329b2b9156",
#     "redirect_url" : "https://localhost:3000",
#     "code" : "TYiBzyokPg9_FHfkqTmZslK_rI71gq_XIo7XeA8blVe9b8LQrjNFj8UV4eUxVaCXRTd7CQo9cxcAAAF_-eERHw"
# }
data = { #--> for refesh token
    "grant_type" : "refresh_token",
    "client_id" : "4978360da1e4f3d72f005c329b2b9156", #--> rest api key
    "redirect_url" : "https://localhost:3000",
    "refresh_token" : "TXEbNhraRILSqc5fXt3Vhd5VHHARJLJ4jstpugo9dVoAAAF_-eMFsA" #--> refresh token
}
response = requests.post(url, data=data)
j_son = response.json()
tokens = j_son.get('access_token')
print(tokens)

# uuid: EyEXLxwlFiQQPA01BjMFNQI0BCgfLRoqGixh

'''
{'access_token': 'O9M2OnnQmbyujsd6I5V6MGQW1muihGFQwnG_fQo9dVoAAAF_-eMFsQ', 'token_type': 'bearer', 'refresh_token': 'TXEbNhraRILSqc5fXt3Vhd5VHHARJLJ4jstpugo9dVoAAAF_-eMFsA', 'expires_in': 21599, 'scope': 'profile_image talk_message profile_nickname friends', 'refresh_token_expires_in': 5183999}
'''

# https://kauth.kakao.com/oauth/authorize?client_id={REST API 키}&redirect_uri=https://localhost:3000&response_type=code&scope=talk_message
# https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=4978360da1e4f3d72f005c329b2b9156&redirect_uri=https://localhost:3000
# https://localhost:3000/?code=TYiBzyokPg9_FHfkqTmZslK_rI71gq_XIo7XeA8blVe9b8LQrjNFj8UV4eUxVaCXRTd7CQo9cxcAAAF_-eERHw
