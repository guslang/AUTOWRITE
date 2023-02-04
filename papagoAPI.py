import os
import sys
import requests
import papagoID

client_id = papagoID.client_id           # 네이버에서 발급받은 client id
client_secret = papagoID.client_secret   # 네이버에서 발급받은 client_secret
# 파파고 API 번역
def translate(text, src="ko", tgt="en"):
    # data = encText
    url = "https://openapi.naver.com/v1/papago/n2mt"    
    #요청 헤더
    req_header = {"X-Naver-Client-Id":client_id, "X-Naver-Client-Secret":client_secret}
    #요청 파라메터
    req_param = {"source":src, "target":tgt, "text":text}
    #번역 요청
    res = requests.post(url, headers=req_header, data=req_param)
    #결과 출력
    trans_txt = ""
    if res.status_code == 200 :
        # print(type(res.text),res.text)
        # print(type(res.json()), res.json())
        trans_txt = res.json()['message']['result']['translatedText']
        print(trans_txt)
    else:
        print("error code", res.status_code)
    return trans_txt
