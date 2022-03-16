from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json,requests
from googletrans import Translator

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('QENbrXK2ILlWZcsE66gdCG9JZErWh89eaiba8ca9cpbIg+Ief6A6XgOuXIQlB0Z0D6InAMaZeoUf2wp7O9CZFNtZP5CNUW6JxRqOtJLczNGI/za2aNxvPUgAwDDe99vIQPzP7A9ckaS95cSN6oaSKQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8d69c575546b27890e4fd909143a8e8c')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

cities = ['基隆市','嘉義市','臺北市','嘉義縣','新北市','臺南市','桃園市','高雄市','新竹市','屏東縣','新竹縣','臺東縣','苗栗縣','花蓮縣','臺中市','宜蘭縣','彰化縣','澎湖縣','南投縣','金門縣','雲林縣','連江縣']
import twder

currencies={'美金':'USD','美元':'USD','港幣':'HKD','英鎊':'GBP','澳幣':'AUD','加拿大幣':'CAD',\
    '加幣':'CAD','新加坡幣':'SGD','新幣':'SGD','瑞士法郎':'CHF','瑞郎':'CHF','日國':'JPY',\
    '日幣':'JPY','南非幣':'ZAR','瑞典幣':'SEK','紐元':'NZD','紐幣':'NZD','泰幣':'THB',\
    '泰銖':'THB','菲國比索':'PHP','菲國賓幣':'PHP','印尼幣':'IDR','歐元':'EUR','韓元':'KRW',\
    '韓幣':'KRW','越南盾':'VND','越南幣':'VND','馬來幣':'MYR','人民幣':'CNY'}
keys = currencies.keys()

def get(city):
    token = 'CWB-E86446FB-80A5-4626-B3FD-A61BBE114060'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    Data = (json.loads(Data.text,encoding='utf-8'))['records']['location'][0]['weatherElement']
    res = [[] , [] , []]
    for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
    return res

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    
    a=[]
    text=message
    a=text.split(':',1)
    translator = Translator()
    if (a[0]=='0'):
        result = translator.translate(a[1],dest='zh-TW').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='1'):
        result = translator.translate(a[1],dest='en').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='2'):
        result = translator.translate(a[1],dest='ja').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='3'):
        result = translator.translate(a[1],dest='ko').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='4'):
        result = translator.translate(a[1],dest='fr').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='5'):
        result = translator.translate(a[1],dest='de').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='6'):
        result = translator.translate(a[1],dest='ru').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
    elif (a[0]=='7'):
        result = translator.translate(a[1],dest='th').text
        line_bot_api.reply_message(reply_token,TextSendMessage(text=result))
        
    tlist = ['現金買入','現金賣出','即期買入','即期賣出']
    currency = message
    show = currency + '匯率:\n'
    if currency in keys:
        for i in range(4):
            exchange = float(twder.now(currencies[currency])[i+1])
            show = show + tlist[i] + ':' + str(exchange) + '\n'
        line_bot_api.reply_message(reply_token,TextSendMessage(text=show))
    #print(show)
    '''else:
        line_bot_api.reply_message(reply_token,TextSendMessage(text="無此貨幣資料!"))
        #print('無此貨幣資料!')'''
    
    if(message[:2] == '天氣'):
        city = message[3:]
        city = city.replace('台','臺')
        if(not (city in cities)):
            line_bot_api.reply_message(reply_token,TextSendMessage(text="查詢格式為: 天氣 縣市"))
        else:
            res = get(city)
            line_bot_api.reply_message(reply_token, TemplateSendMessage(
                alt_text = city + '未來 36 小時天氣預測',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url = 'https://i.imgur.com/Ex3Opfo.png',
                            title = '{} ~ {}'.format(res[0][0]['startTime'][5:-3],res[0][0]['endTime'][5:-3]),
                            text = '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {}'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                            actions = [
                                URIAction(
                                    label = '詳細內容',
                                    uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                )
                            ]
                        )for data in res
                    ]
                )
            ))
    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="查詢格式為: 天氣 縣市\n輸入貨幣名稱 ex:美元、歐元\n翻譯格式:\n中文 0:欲翻譯之句子\n英文 1:欲翻譯之句子\n日文 2:欲翻譯之句子\n韓文 3:欲翻譯之句子\n法文 4:欲翻譯之句子\n德文 5:欲翻譯之句子\n俄文 6:欲翻譯之句子\n泰文 7:欲翻譯之句子"))

if __name__=='__main__':
    app.run()