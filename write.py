import requests
import json
from bs4 import BeautifulSoup
import datetime as dt

# tstory API 정보
client_id = "5c172c85dcc41719296c3dd42e70c1bb"
client_secret = "5c172c85dcc41719296c3dd42e70c1bbd1dee70946aca5b88ddbbce369a9c8eec4618c10"
access_token = "cdccd5c9b895b49e136acebf803b6d63_84db324c29db22f91365356fde89ce7d"
redirect_uri = "http://nocrazy.tistory.com/"
blogName = "nocrazy"
categoryId = "1059536" 

# 글 작성
# https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html
def postWrite(blog_name, title, content="", visibility=None, category_id=None, published=None, slogan=None, tag=None,
              acceptComment=None, password=None, output_type="json"):
    url = "https://www.tistory.com/apis/post/write?"
    data = {}
    data['access_token'] = access_token
    data['output'] = output_type
    data['blogName'] = blog_name
    data['title'] = title
    data['content'] = content
    if visibility is not None:
        url += "visibility=" + visibility + "&"
    if category_id is not None:
        url += "category=" + category_id + "&"
    if published is not None:
        url += "published=" + published + "&"
    if slogan is not None:
        url += "slogan=" + slogan + "&"
    if tag is not None:
        url += "tag=" + tag + "&"
    if acceptComment is not None:
        url += "acceptComment=" + acceptComment + "&"
    if password is not None:
        url += "password=" + password
    res = requests.post(url, data=data).content
    # return json.loads(res)
    return res

if __name__ == "__main__":
    # 현재 날짜 가져오기
    x = dt.datetime.now()
    today = str(x.year) + '-' + str(x.month) + '-' + str(x.day)
    
    url = 'http://www.yes24.com/24/Category/BestSeller?CategoryNumber=001&sumgb=06'
    t_title = "YES24 종합 베스트셀러 Top 10(" + today +")"
        
    # url 정보 수집하기
    response = requests.get(url)
    
    # status_code가 200이면 정상
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')        
    else : 
        print(response.status_code)
         
    j = 1
    k = 2  
    contentAll = ""
    for i in range(1,11,1):
        # 제목          
        bookTitle_tag ='#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.goodsTxtInfo > p:nth-child(1) > a:nth-child(1)'                                               
        bookTitles = soup.select(bookTitle_tag)
        bookTitle = bookTitles[0].text        
        # 저자/출판사/발행월
        auth_tag = '#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.goodsTxtInfo > div'            
        auths = soup.select(auth_tag)
        auth = auths[0].text.replace('\n', ' ').replace('\r', '').replace('\t','').strip()               
        # 가격/
        price_tag ='#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.goodsTxtInfo > p:nth-child(3)'
        prices = soup.select(price_tag)
        price = prices[0].text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()        
        # 요약
        summary_tag = '#category_layout > tbody > tr:nth-child(' + str(k) + ') > td:nth-child(2) > p'
        summarys = soup.select(summary_tag)
        summary = summarys[0].text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()        
        # 이미지                      
        bookImg_tag ='#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.image > div > a:nth-child(1) > img'
        bookImgs = soup.select(bookImg_tag)
        bookImg = bookImgs[0].text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()        
        bookImg = (bookImgs[0].attrs['src'].split('/'))[4]      
        
        # 출력 포맷     
        content  = '<h3 data-ke-size="size23"><b>' + str(i) + '. ' + bookTitle + '</b></h3>'
        content += '<ul style="list-style-type: disc;" data-ke-list-type="disc">'        
        content += '<li>' + auth + '</li>'
        content += '<li>' + price + '</li>'
        content += '<li>' + summary + '</li>'
        content += '</ul>'
        content += '<figure data-ke-type="emoticon" data-ke-align="alignCenter" data-emoticon-isanimation="false"><img src="https://image.yes24.com/goods/' + \
            bookImg +'/L" width="300" alt="' + bookTitle + '"/></figure>'        
        content += '<P> </P>'        
        contentAll += content
        j = j + 2
        k = k + 2
                
    tagName = "YES24,자기계발,자동포스팅"
    visiblityCd = "0"    # 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
    publishedDt = None   # 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)    
    # 티스토리 API 이용하여 포스트 등록
    postWrite(blog_name=blogName, title=t_title, content=contentAll, visibility=visiblityCd, category_id=categoryId, published=publishedDt, 
                         slogan=None, tag=tagName, acceptComment=None, password=None, output_type="json")
    
    print("글 등록 완료")