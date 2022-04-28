import requests
import json
from config import telegramBotToken

def sendTelegramMsg(chat_id, input):
    url = "https://api.telegram.org/bot{}/sendMessage".format(telegramBotToken)

    payload = {
        "chat_id": chat_id,
        "text": input
    }

    r = requests.get(url, params=payload)

    # print(r.text)

def getTelegramMsg():
    url = "https://api.telegram.org/bot{}/getUpdates".format(telegramBotToken)

    r = requests.get(url)

    load_json = json.loads(r.text)
    data = load_json['result']
    for i in data:
        print('{:2} {} {} {}'.format(i['message']['message_id'], i['message']['from']['id'], i['message']['from']['username'], i['message']['text']))