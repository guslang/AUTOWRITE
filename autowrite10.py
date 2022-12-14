import requests
from bs4 import BeautifulSoup
import datetime as dt

# tstory API 정보
access_token = "티스토리 API Access-Token 입력"
blogName = "블로그 이름(XXX) 입력 : http://XXX.tistory.com/"
categoryId = "블로그 카테고리번호" 

# 티스토리에서 제공한 글 작성 API 호출을 위한 함수
# API : https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html
def postWrite(blog_name, title, content="", visibility=None, category_id=None, published=None, 
              slogan=None, tag=None, acceptComment=None, password=None, output_type="json"):
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

# 프로그램 시작하는 지점 - MAIN
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
         
    # Top 10 순서 정보를 가져오기 위한 변수
    j = 1
    k = 2  
    # HTML코드로 작성된 Top 10 정보 저장 변수
    contentAll = ""
    # 1위부터 10위까지 베스트 셀러 정보 가져오기
    for i in range(1,11,1):
        # 제목          
        bookTitles = soup.select('#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.goodsTxtInfo > p:nth-child(1) > a:nth-child(1)')
        bookTitle = bookTitles[0].text        
        # 저자/출판사/발행월
        auths = soup.select('#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.goodsTxtInfo > div')
        auth = auths[0].text.replace('\n', ' ').replace('\r', '').replace('\t','').strip()               
        # 가격/        
        prices = soup.select('#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.goodsTxtInfo > p:nth-child(3)')
        price = prices[0].text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()        
        # 요약
        summarys = soup.select('#category_layout > tbody > tr:nth-child(' + str(k) + ') > td:nth-child(2) > p')
        summary = summarys[0].text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()        
        # 이미지                              
        bookImgs = soup.select('#category_layout > tbody > tr:nth-child(' + str(j) + ') > td.image > div > a:nth-child(1) > img')
        bookImg = (bookImgs[0].attrs['src'].split('/'))[4]      # '/' 기준으로 이미지 URL을 구분하여 5번째 정보(ID)를 가져온다.
        
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
