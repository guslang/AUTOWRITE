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
    # 추천도서를 가져올 웹사이트 URL 정보
    url = 'http://www.yes24.com/24/Category/Display/001005033043'
    t_title = "당신을 위한 오늘의 추천 도서 (" + today +")"
        
    # url 정보 수집하기
    response = requests.get(url)
    
    # status_code가 200이면 정상
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')        
    else : 
        print(response.status_code)
    
    # 제목          
    bookTitles = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_name > a:nth-child(2)')
    bookTitle = bookTitles[0].text.strip()        
    # 저자
    auths = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_pubGrp > span.goods_auth')
    auth = auths[0].text.strip()
    # 가격
    prices = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_price > em.yes_b')
    price = prices[0].text.strip() + '원'
    # 요약
    summarys = soup.select('#category_layout > ul > li:nth-child(1) > div > div.goods_info > div.goods_read')
    summary = summarys[0].text.strip()
    # 이미지                      
    bookImgs = soup.select('#category_layout > ul > li:nth-child(1) > div > p > span > span > a > img')
    bookImg = bookImgs[0].attrs['src']   
    
     # 출력 포맷     
    content =  '<h3 data-ke-size="size23"><i>오늘(' +today+ ') 당신을 위한 YES24 추천도서입니다.</i><b></b></h3>'
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
    tagName = "YES24,자기계발,자동포스팅"
    visiblityCd = "0"    # 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
    publishedDt = None   # 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)    
    # 티스토리 API 이용하여 포스트 등록
    postWrite(blog_name=blogName, title=t_title, content=content, visibility=visiblityCd, category_id=categoryId, 
               published=publishedDt, slogan=None, tag=tagName, acceptComment=None, password=None, output_type="json")
    
    print("글 등록 완료")
