import requests
from bs4 import BeautifulSoup
import datetime as dt
import sys
import tistoryAPI
import blogInfo
import papagoAPI
import papagoID

# 프로그램 시작하는 지점 - MAIN
if __name__ == "__main__":
    # 현재 날짜 가져오기
    x = dt.datetime.now()
    today = str(x.year) + '-' + str(x.month) + '-' + str(x.day)
    # 추천도서를 가져올 웹사이트 URL 정보
    url = 'http://www.yes24.com/24/Category/Display/001005033043'
    t_title = "당신을 위한 오늘의 추천 도서 (" + today +")"
    t_title = papagoAPI.translate(t_title) 
        
    # url 정보 수집하기
    response = requests.get(url)
    
    # status_code가 200이면 정상
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')        
    else : 
        print(response.status_code)
        sys.exit(0)
    
    # 제목          
    bookTitles = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_name > a:nth-child(2)')    
    bookTitle = papagoAPI.translate(bookTitles[0].text.strip()) + "(" + bookTitles[0].text.strip() +")"
    # 저자
    auths = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_pubGrp > span.goods_auth')
    auth = papagoAPI.translate(auths[0].text.strip()) + "(" + auths[0].text.strip() +")"    
    # 가격
    prices = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_price > em.yes_b')
    price = papagoAPI.translate(prices[0].text.strip() + '원')    
    # 요약
    summarys = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_read')
    summary = papagoAPI.translate(summarys[0].text.strip())
    # 이미지                      
    bookImgs = soup.select('#category_layout > ul > li:nth-child(1) > div > p > span > span > a > img')
    bookImg = bookImgs[0].attrs['src']   
    
    intro_title = '오늘(' +today+ ') 당신을 위한 YES24 추천도서입니다.'
    intro_title = papagoAPI.translate(intro_title)
    
     # 출력 포맷     
    content =  '<h3 data-ke-size="size23"><i>' + intro_title + '</i><b></b></h3>'
    content += '<h3 data-ke-size="size23"><b>'+ bookTitle + '</b></h3>'
    content += '<ul style="list-style-type: disc;" data-ke-list-type="disc">'        
    content += '<li>' + auth + '</li>'
    content += '<li>' + price + '</li>'
    content += '<li>' + summary + '</li>'
    content += '</ul>'
    content += '<figure data-ke-type="emoticon" data-ke-align="alignCenter" data-emoticon-isanimation="false">' \
     '<img src="' + bookImg +'" width="300" alt="' + bookTitle + '"/></figure>'        
    content += '<P> </P>'        
    
    #티스토리 태그정보 입력            
    tagName = "BestSeller,PassiveIncome,AutoMation"
    visiblityCd = "0"    # 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
    publishedDt = None   # 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)    
    # 티스토리 API 이용하여 포스트 등록
    
    try :
        tistoryAPI.postWrite(blogInfo.access_token, blog_name=blogInfo.blogName, title=t_title, content=content, visibility=visiblityCd, category_id=blogInfo.categoryId, 
              published=publishedDt, slogan=None, tag=tagName, acceptComment=None, password=None, output_type="json")
        print("글 등록 완료")
    except Exception as e: 
        print('예외가 발생했습니다.', e)
