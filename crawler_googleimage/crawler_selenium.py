from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib.request
import pickle

with open('train_question.pkl', 'rb') as f:
    data = pickle.load(f)

options = webdriver.ChromeOptions()
options.add_argument('headless')

for idx, searchterm in enumerate(data):
    # 찾고자 하는 검색어를 url로 만들어 준다.
    # searchterm = 'person'
    if idx <= 5064 :
        continue
    url = "https://www.google.com/search?q=" + searchterm + "&source=lnms&tbm=isch"
    # chrom webdriver 사용하여 브라우저를 가져온다..
    browser = webdriver.Chrome('C:/Users/dilab/PycharmProjects/crawler-cqa/chromedriver', chrome_options=options)
    # browser = webdriver.Chrome('./chromedriver/chromedriver')
    browser.get(url)

    # User-Agent를 통해 봇이 아닌 유저정보라는 것을 위해 사용
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    # 이미지 카운트 (이미지 저장할 때 사용하기 위해서)
    counter = 0
    succounter = 0

    print(os.path)
    # 소스코드가 있는 경로에 '검색어' 폴더가 없으면 만들어준다.(이미지 저장 폴더를 위해서)
    if not os.path.exists(searchterm):
        os.mkdir(searchterm)

    for _ in range(500):
        # 가로 = 0, 세로 = 10000 픽셀 스크롤한다.
        browser.execute_script("window.scrollBy(0,10000)")
    import socket
    # div태그에서 class name이 rg_meta인 것을 찾아온다
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        counter = counter + 1
        print("Total Count:", counter)
        print("Succsessful Count:", succounter)
        print("URL:", json.loads(x.get_attribute('innerHTML'))["ou"])

        # 이미지 url
        img = json.loads(x.get_attribute('innerHTML'))["ou"]
        # 이미지 확장자
        imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]

        # 구글 이미지를 읽고 저장한다.
        try:
            req = urllib.request.Request(img, headers=header)
            raw_img = urllib.request.urlopen(req, timeout=5).read()
            File = open(os.path.join(searchterm, searchterm + "_" + str(counter) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succounter = succounter + 1
        except :
            print('timeout')
            continue
        #     print("can't get img")
        if succounter == 300:
            break

    print(succounter, "succesfully downloaded")
    browser.close()
    data_dir = 'C:/Users/dilab/PycharmProjects/crawler-cqa/'
    new_dir = str(idx)
    os.rename(data_dir+searchterm, data_dir+new_dir)

