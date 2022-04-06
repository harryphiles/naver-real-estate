import requests
import json

def sendTelegramMsg(chat_id, input):
    token = '5135359247:AAHC9Up6lUZ8nkw4OllQrAu6lF9xQ1xzgHk'
    url = "https://api.telegram.org/bot{}/sendMessage".format(token)

    payload = {
        "chat_id": chat_id, #"1726140050",
        "text": input
    }

    r = requests.get(url, params=payload)

    print(r.text)

def getTelegramMsg():
    token = '5135359247:AAHC9Up6lUZ8nkw4OllQrAu6lF9xQ1xzgHk'
    url = "https://api.telegram.org/bot{}/getUpdates".format(token)

    r = requests.get(url)

    load_json = json.loads(r.text)
    data = load_json['result']
    for i in data:
        print('{:2} {} {} {}'.format(i['message']['message_id'], i['message']['from']['id'], i['message']['from']['username'], i['message']['text']))

getTelegramMsg()
# sendTelegramMsg('2022415076', "King받네") #"1726140050" # 2022415076