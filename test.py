import requests
from bs4 import BeautifulSoup
import sys

# url 정보 수집하기
url = 'https://www.yes24.com/Product/Category/BestSeller?CategoryNumber=001&sumgb=06'
response = requests.get(url)

# status_code가 200이면 정상
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')        
else : 
    print(response.status_code)
    sys.exit(0)
    
# 제목          
bookTitles = soup.select('#yesBestList > li:nth-child(1) > div > div.item_info > div.info_row.info_name > a.gd_name')
bookTitle = bookTitles[0].text  
print(bookTitle)
