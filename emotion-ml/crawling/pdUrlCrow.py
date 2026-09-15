from bs4 import BeautifulSoup
from numpy import NaN
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


import pandas as pd

# 1. 박스 오피스 순위의 영화명을 추출
df = pd.read_excel('box_office.xlsx')
df_sample = df.loc[:, '영화명'].tolist()
print(df_sample)

# 영화명에 대한 url을 담을 리스트 준비
url_List = []

# for i in range(len(df_sample)):
#
#     count = len(df_sample) - i
#     print(count)
#
#     #2. 셀레니움 준비부분
#     url = 'https://movie.daum.net/main'
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(url)
#     html = driver.page_source  # 드라이버 html에 설정
#     soup = BeautifulSoup(html, 'html.parser')  # soup 설정은 똑같음
#     driver.set_window_size(1200, 685)
#     driver.implicitly_wait(1)
#     time.sleep(1)
#
#     #3. 다음 홈페이지에서 검색 클릭 후 박스오피스의 '영화명' 검색 후, 영화 소개 홈페이지를 들어감, 영화 인덱스의 url 추출 하여 url List에 담음
#     try:
#         more_btn = driver.find_element(by=By.NAME,value='q')
#         more_btn.send_keys(df_sample[i] + Keys.ENTER)
#         more = driver.find_elements(by=By.CSS_SELECTOR,value=
#                     '#mainContent > div > div.box_searchinfo > div.detail_searchinfo.movie.search_result > ul > li:nth-child(1) > div > a')
#         more[0].click()
#
#         url_List.append(driver.current_url)
#         # print(driver.current_url)
#         driver.close()
#         # print(url_List)
#     except:
#         url_List.append(NaN)
#         driver.close()
#
#
# # url_list 를 저장
# df_result = df.assign(name = df_sample, url = url_List )
# df_result.to_excel('box_office.xlsx')
# print(df_result)



