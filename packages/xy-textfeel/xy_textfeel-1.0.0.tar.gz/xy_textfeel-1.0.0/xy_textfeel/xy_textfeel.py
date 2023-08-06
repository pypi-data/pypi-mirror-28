import requests
import json
import base64
import math

'''文字意图分析'''
def textfeel(text=''):
    FEEL_DESC = {-1:'负面',0:'中性',1:'正面'}

    if not text:
        return -1
    url = 'https://www.phpfamily.org/textfeel.php'
    data = {}
    data['text']=text
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        res_dict = {}
        res_dict['text']=res['data']['text']
        res_dict['feel']=FEEL_DESC[res['data']['polar']]
        positive = math.ceil(res['data']['confd']*100)
        res_dict['positive']=str(positive) + '%'
        res_dict['negative']=str(100-positive) + '%'
        return res_dict
    else:
        return -1



def main():
    res = textfeel('这家日料的食材特别新鲜，跟朋友一起吃得很开心很满足。')
    print(res)


if __name__ == '__main__':
    main()
