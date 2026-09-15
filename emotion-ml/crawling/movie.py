from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import time
import string
from selenium.webdriver.common.by import By
import random

import pandas as pd

# ─────────────────────────────────────────────
# 설정 (원본은 개인 로컬 절대경로가 하드코딩되어 있었음 → 상대경로 + webdriver-manager로 교체)
BOX_OFFICE_PATH = 'box_office2.xlsx'  # 스크립트와 같은 폴더 기준 상대경로
OUTPUT_PATH = 'crowMovies.xlsx'
CHROME_SERVICE = Service(ChromeDriverManager().install())  # chromedriver 자동 설치/버전 매칭
# ─────────────────────────────────────────────

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['제목','개봉','장르','국가','등급','러닝타임','평점','누적관객','박스오피스','영화포스터url','배우','배우url','줄거리','리뷰'])
url_source = ['grade', 'main']

# 박스오피스 데이터
df = pd.read_excel(BOX_OFFICE_PATH)
# pandaslist를 일반list로 변경
url_list = [''.join(map(str,i)) for i in df['url']]

num = 0
for i in range(len(url_list)):
    time.sleep(random.randrange(0,2))
    num += 1
    # sNum = str(num)
    print(num,'번째 영화 시작')

    url = url_list[i].replace('main','grade')
    html = urlopen(url)
    # print(url)
    soup = BeautifulSoup(html, "html.parser")

    # 영화여부가 1순위, 없으면 다른영화

    try:
        title = soup.select_one('#mainContent > div > div.box_basic > div.info_detail >'
                            ' div.detail_tit > h3 > span.txt_tit').text.strip()
    except:
        print('영화가 없습니다.')
        continue
    print(title)

    # # 리뷰----------------- 셀리니움부분 --------------------------------------
    driver = webdriver.Chrome(service=CHROME_SERVICE)
    driver.get(url)
    html = driver.page_source  # 드라이버 html에 설정
    soup = BeautifulSoup(html, 'html.parser')  # soup 설정은 똑같음

    driver.set_window_size(1200, 685)
    driver.implicitly_wait(3)


    review_list = []
    review_NMZ = []
    review_result = []

    # 리뷰 더보기 클릭 부분, 더 없을시 다음 단계 진행
    for j in range(15):
        try:
            more_btn = driver.find_elements(by=By.CSS_SELECTOR,value=
            '#alex-area > div > div > div > div.cmt_box > div.alex_more > button')
            more_btn[0].click()
            driver.implicitly_wait(1)
        except:
            break

    #리뷰 추출
    try:
        reviews = driver.find_elements(By.CSS_SELECTOR, '#alex-area > div > div > div > div.cmt_box > ul.list_comment')
    except:
        continue
    # \n 기준 분리, 문자열 형태로 빼냄
    for review in reviews:
        review_list.append(review.text.split('\n'))
        # print(review_list)
    try:
        new_review = " ".join(review_list[0])
    except:
        print('리뷰가 없습니다. 다음 홈페이지')
        continue
    # print(new_review)

    # for 문 밖으로 뺴버리면 처음만 전처리 되고 그다음부턴 안됨.
    del_str = ['댓글 찬성하기', '댓글 비추천하기', '.', ':']
    for c in string.ascii_letters:
        del_str.append(c)
    for v in string.digits:
        del_str.append(v)

    # 필요 없는 문자 정규화
    for s in del_str:
        new_review = new_review.replace(s,' ')
    review_NMZ.append(new_review.split('  '))
    # print(review_NMZ)

    # 닉네임 길이, 짤린말 특징이 인덱스 15개 이하
    for k in review_NMZ[0]:
        k = k.strip()
        if len(k) >= 20:
            review_result.append(k)

    print('리뷰 갯수 : ', len(review_result))

    if(len(review_result) <= 30):
        print('리뷰 갯수가 모자릅니다. 다음 영화로 넘어갑니다. \n')
        continue


    review_Result2 = ' '.join(review_result)

    #str용
    # print(review_Result2)
    #배열용
    # print(review_result)


    # 아이템들 개봉,장르,국가 등등..
    try:
        html = urlopen(url)
    except:
        print("url 문제, 다음 영화 \n")
        continue
    soup = BeautifulSoup(html, "html.parser")
    Items = soup.select('#mainContent > div > div.box_basic > div.info_detail > div.detail_cont')
    Item_list = []
    Item_listResult = []
    for Item in Items:
        Item_list.append(Item.get_text().replace('\n', ' ').split(' ')) #\n 부분 공백으로
        # print(Item_list)
    while "" in Item_list[0]:
        Item_list[0].remove("") # 공백문자 제거 삭제
    # print(Item_list[0])

    sheet_index = ['개봉', '-', '장르', '-', '국가', '-', '등급', '-', '러닝타임', '-', '평점', '-', '누적관객', '-', '박스오피스', '-']
    for o in range(0, len(sheet_index)):
        for p in range(0, len(Item_list[0])):
            # 문자가 -이거나 - 앞에 인덱스가 같을때..
            if (sheet_index[o] == '-' and sheet_index[o - 1] == Item_list[0][p]):
                sheet_index[o] = Item_list[0][p + 1]

    # print(sheet_index)

    driver.close()

    #메인 페이지로 변경
    driver2 = webdriver.Chrome(service=CHROME_SERVICE)
    url2 = url_list[i]
    # url2 = 'https://movie.daum.net/moviedb/main?movieId=' + sNum
    driver2.get(url2)
    html2 = driver2.page_source  # 드라이버 html에 설정
    soup2 = BeautifulSoup(html2, 'html.parser')  # soup 설정은 똑같음
    # print(url2)

    driver2.set_window_size(1200, 685)
    driver2.implicitly_wait(2)

    # 감독 및 배우 이름
    name_ActorList = []
    del_str = ['감독', '주연', '출연']
    name_Actors = driver2.find_elements(By.CSS_SELECTOR,
                                       '#mainContent > div > div.box_detailinfo > div.contents > div.detail_crewinfo > ul')
    for name_Actor in name_Actors:
        # print(name_Actor.text)
        name_ActorList.append(name_Actor.text)
    # print(name_ActorList)
    # new_nameActor = " ".join(name_ActorList[0])

    for w in del_str:
        name_ActorList[0] = name_ActorList[0].replace(w,'').replace('\n','/').replace('//','/')
    name_ActorResult = ''.join(name_ActorList[0])
    # print(name_ActorResult)

    # 영화 포스터
    Poster_DelText = ['background-image: url("', '");']
    img_PosterResult = []

    img_Posters = driver2.find_elements(By.CSS_SELECTOR,
                                       '#mainContent > div > div.box_basic > div.info_poster > a > span.bg_img')
    for img_Poster in img_Posters:
        img_PosterResult.append(img_Poster.get_attribute('style').split('"'))

    # 포스터 url
    # print(img_PosterResult[0][1])

    #배우 url
    img_ActorList = []
    for n in range(1, 8):
        str__num = str(n)
        try:
            img_Actors = driver2.find_elements(By.CSS_SELECTOR,
                                              '#mainContent > div > div.box_detailinfo > div.contents > div.detail_crewinfo > ul > li:nth-child(' + str__num + ') > div > a > img')
            for img_Actor in img_Actors:
                # print(strnum+'번 배우 '+img_Actor.get_attribute('src'))
                img_ActorList.append(img_Actor.get_attribute('src'))
        except:
            break

    img_ActorResult = " ".join(img_ActorList)

    # 리스트용
    # print(img_ActorList)
    # 엑셀용
    # print(img_ActorResult)

    driver2.implicitly_wait(1)

    #줄거리
    summary_list = []

    summarys = driver2.find_elements(By.CSS_SELECTOR,'#mainContent > div > div.box_detailinfo > div.contents > div.detail_basicinfo > div > div > div')

    try:
        for summary in summarys:
            summary_list.append(summary.text.split('\n'))
        while "" in summary_list[0]:
            summary_list[0].remove("") # 공백문자 제거 삭제
        summary_Result = ' '.join(summary_list[0])
    except:
        print("주요정보 없음, 다음영화 탐색\n")

    # print(summary_Result)

    driver2.close()
    sheet.cell(row=1, column=1)

    try:
        sheet.append([title,sheet_index[1],sheet_index[3],
                      sheet_index[5],sheet_index[7],sheet_index[9],
                      sheet_index[11],sheet_index[13],sheet_index[15],img_PosterResult[0][1],
                      name_ActorResult ,img_ActorResult ,summary_Result , review_Result2])
    except:
        print("인덱스 초과로 업로드 실패, 다음영화 탐색\n")
        continue
    print(i+1," 번째 영화 완료\n")


wb.save(OUTPUT_PATH)
