
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from konlpy.tag import Okt
import requests
import urllib.request
import urllib.error
import random
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

start = time.time()
def hangul_only(s):
    hangul = re.compile('[ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', s)
    result = hangul.findall(s)
    return result

def strip_e(st):
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return RE_EMOJI.sub(r'', st)

stop_words = []
with open("./stopwords.txt", "r",encoding="utf-8") as r:
    lines = r.readlines()
    for line in lines:
        stop_words.append(line.strip())


def crawling_1(tag_search):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/61.0.3163.100 Safari/537.36")

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36")

    DRIVER_DIR = 'C:/Users/dilab/PycharmProjects/crawler-cqa/chromedriver'


    url = 'https://www.instagram.com/accounts/login/?hl=ko'
    driver = webdriver.Chrome(DRIVER_DIR, options=options)
    driver.get(url)
    time.sleep(1)



    element = driver.find_element_by_name("username")
    element.send_keys('01099040959')
    element = driver.find_element_by_name("password")
    element.send_keys('09590959')
    element.submit()
    time.sleep(3)
    # //*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input

    # log_but2 = "//button[contains(@class, 'aOOlW   HoLwm ') and text()='나중에 하기']"
    # driver.find_element_by_xpath(log_but2).click()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div/div').click()
    driver.implicitly_wait(3)

    email_box = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    email_box.send_keys(tag_search)
    email_box = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]')
    email_box.click()

    # driver.find_element(By.CLASS_NAME("XTCLo.x3qfX")).sendKeys("데일리룩");
    # driver.find_element_by_class_name("XTCLo.x3qfX").sendKeys('데일리룩')

    # driver.find_element_by_name("username").send_keys("01099040959")
    # driver.find_element_by_name("password").send_keys("09590959")
    # driver.find_element_by_xpath("//div/form/div[4]/button/div").submit()




    SCROLL_PAUSE_TIME=2
    reallink = []
    a=0
    while(a<=50):
        b=0
        while (b ==0):

            pageString = driver.page_source
            bsObj = BeautifulSoup(pageString, "lxml")
            b = b + 1
            d=0
            reallink_1=[]
            for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
                d=d+1
                reallinks = []
                if 1<=len(link1.select('a')):
                    title = link1.select('a')[0]
                    real = title.attrs['href']
                    reallinks.append(real)
                if 2<=len(link1.select('a')):
                    title = link1.select('a')[1]
                    real = title.attrs['href']
                    reallinks.append(real)
                if 3<=len(link1.select('a')):
                    title = link1.select('a')[2]
                    real = title.attrs['href']
                    reallinks.append(real)
                reallink_1.extend(reallinks)
                print(" link time :", time.time() - start)
            print(reallink_1)
            if(d!=1):
                reallink_1=reallink_1[9:]
            reallink.extend(reallink_1)
            print(reallink_1)



        a=a+1
        c=0
        while(c==0):


            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            c=c+1
    return reallink



# print(len(reallink))


hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

# request.close()
# request.keep_alive
# request.time.sleep

tag_list = ['데일리룩','오오티디','패션','옷스타그램','패션스타그램','옷','데일리','코디','패피','데이트룩','빈티지',
       '먹스타그램','맛스타그램','맛집','먹방','술스타그램','먹스타','맛있다그램','먹부림','요리','푸드스타그램',
       '육아','육아스타그램','육아','소통','육아맘','맘스타그램','딸스타그램','도치맘','아들스타그램','애스타그램',
       '젊줌마','여행','여행스타그램','여행에미치다','가족여행','제주여행','일본여행','유럽여행','제주도여행','부산여행',
       '해외여행','멍스타그램','반려견','강아지','고양이','냥스타그램','개스타그램','펫스타그램','독스타그램','댕댕이',
       '개린이','다이어트','운동','운동하는여자','헬스타그램','헬스','운동하는남자','전신샷','필라테스','요가','식단',
       '뷰티','뷰티스타그램','메이크업','화장품','코덕','손스타그램','뷰스타그램','뷰티그램','인스타','부티템']


# req = urllib.request.Request(img, headers=header)
# raw_img = urllib.request.urlopen(req, timeout=5).read()

def crawling_2(reallink, tag):
    for i in range(len(reallink)):

        with open("./insta_hashtag_"+tag+".txt", 'a', encoding='utf-8', errors='ignore') as f:
            texts = []
            hashtags = []
            try:
                req = urllib.request.Request('https://www.instagram.com/p' + reallink[i], headers=hdr)
                webpage_0 = urllib.request.urlopen(req, timeout=1000)
                webpage = webpage_0.read()
                webpage_0.close()

                # webpage = urllib.request.urlopen('https://www.instagram.com/p' + reallink[i]).read()
                soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
                # print("url open time :", time.time() - start)
            except:
                break


            # except  urllib.error.HTTPError as e:
            #     print(e.reason)
            # except urllib.error.URLError as e:
            #     print(e.reason)
            soup1 = soup.title.find(string=True)
            soup1 = soup1[soup1.find(':') + 1:]
            soup1 = soup1.strip()
            text = [soup1[1:-1]]
            # okt = Okt()
            soup1=strip_e(soup1)
            # okt_morphs = okt.pos(soup1)
            words = []

            for word in soup1:
                words.append(word)

            hashtag = []

            for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
                reallink2 = reallink2['content']
                reallink2=strip_e(reallink2)
                reallink2 = hangul_only(reallink2)
                if reallink2 != []:
                    hashtag.append(''.join(reallink2))


            if words != [] and hashtag != []:
                print(hashtag)
                f.write(' '.join(words) + '\t' + ' '.join(hashtag) + '\n')
                # print("end time :", time.time() - start)



for idx in range(56, 10000):
    index = idx % len(tag_list)
    tag = tag_list[index]
    link = crawling_1(tag)
    crawling_2(link, tag)


