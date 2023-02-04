import requests
from bs4 import BeautifulSoup

# url 정보 수집하기
url = 'http://www.yes24.com/24/Category/BestSeller?CategoryNumber=001&sumgb=06'
response = requests.get(url)

# status_code가 200이면 정상
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html5lib')        
else : 
    print(response.status_code)
    
# 제목          
bookTitles = soup.select('#category_layout > tbody > tr:nth-child(1) > td.goodsTxtInfo > p:nth-child(1) > a:nth-child(1)')
bookTitle = bookTitles[0].text  
print(bookTitle)
