import requests
import os, json

# 글 작성
# https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html
def postWrite(access_token, blog_name, title, content="", visibility=None, category_id=None, published=None, slogan=None, tag=None,
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
    return res
