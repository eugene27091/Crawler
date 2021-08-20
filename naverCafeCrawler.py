from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip
import datetime

driver = webdriver.Chrome("./chromedriver")

driver.get('https://www.naver.com/')
time.sleep(1)

# 로그인 버튼을 찾고 클릭합니다
login_btn = driver.find_element_by_class_name('link_login')
login_btn.click()
time.sleep(1)

# id, pw 입력할 곳을 찾습니다.
tag_id = driver.find_element_by_name('id')
tag_pw = driver.find_element_by_name('pw')
tag_id.clear()
time.sleep(1)

# id 입력
tag_id.click()
pyperclip.copy('eugene27091')
tag_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# pw 입력
tag_pw.click()
pyperclip.copy('2470627j@@')
tag_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 로그인 버튼 클릭
login_btn = driver.find_element_by_id('log.login')
login_btn.click()


title_list = []
content_list = []
nickname_list = []
date_list = []
comment_content_list = []
comment_nickname_list = []
comment_date_list = []


# 크롤링 시작
def crawling():
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    a_hrefs = soup.find_all("a", "article")  # class = article 에 href가 있어서 가져왔습니다.

    basic_url = "https://cafe.naver.com"  # 기본 url
    for a in a_hrefs:  # a_hrefs에 href만 가져와서 받아온 수 만큼 돌립니다. ( 한페이지에 15개씩 지금은 2페이지 받아와서 30번입니다.)
        detail_url = basic_url + a['href']
        print(detail_url)  # 예시 출력
        driver.get(detail_url)
        driver.switch_to.frame("cafe_main")

        title = driver.find_element_by_class_name('title_text')  # 타이틀 원소를 가져와서 출력하는 부분
        title_list.append(title.text)

        nickname = driver.find_element_by_class_name('nickname')  # 닉네임 원소를 가져와서 출력하는 부분
        nickname_list.append(nickname.text)

        date = driver.find_element_by_class_name('date')  # 날짜 원소를 가져와서 출력하는 부분
        date_list.append(date.text)
        # print()

        # 수정중에 있습니다. 게시글 내용
        # print("*********게시글 내용*********")
        try:  # 본문이 se-main-container 타입인 경우
            cont_explanation = driver.find_element_by_class_name('se-main-container').text
            content_list.append(cont_explanation)
        except NoSuchElementException:  # 본문이 ContentRenderer 타입인 경우
            cont_explanation = driver.find_element_by_class_name('ContentRenderer').text
            content_list.append(cont_explanation)


        if bool(driver.find_elements_by_class_name(
                'text_comment')):  # 댓글이 없는경우도 있어서 bool 함수로 true, false를 반환시킴 댓글이 있으면 true, 없으면 false입니다.

            text_comments = driver.find_elements_by_class_name('text_comment')  # 댓글 원소를 가져와서 출력하는 부분
            for text_comment in text_comments:  # 댓글이 여러개 있을 경우도 있으므로 여러번 출력
                 comment_content_list.append(text_comment.text)

            nickname_comments = driver.find_elements_by_class_name('comment_nickname')
            for nickname_comment in nickname_comments:  # 댓글이 여러개 있을 경우도 있으므로 여러번 출력
                comment_nickname_list.append(nickname_comment.text)

            date_comments = driver.find_elements_by_class_name('comment_info_date')
            for date_comment in date_comments:  # 댓글이 여러개 있을 경우도 있으므로 여러번 출력
                comment_date_list.append(date_comment.text)





        # print()
    print(title_list,content_list ,nickname_list ,date_list )
    print(comment_content_list ,comment_nickname_list ,comment_date_list)

    today = date.today()   # 오늘 날짜 저장
    filename = f'Coupang_3to5_{today.year}_{today.month}_{today.day}'   # 파일 이름 설정
    # item_data_list = getAllItemData()   # getAllItemData  함수에 반환되는 값을 item_data_list 저장
    # item_name, item_function, star_rating, review_num, review_list
    main_list = []   # main_list 초기화
    for item_data in item_data_list:
        main_list.append([item_data['item_name'], item_data['item_function'], item_data['star_rating'], item_data['review_num'], item_data['review_name'], item_data['review_day'], item_data['review_content']])
        # main_list 배열에 위 매개변수 추가하기

    df = pd.DataFrame(main_list)   # pd.DataFrame 생성
    df.columns = ['item_name', 'item_function', 'star_rating','review_num','review_name', 'review_day', 'review_content']   # columns 설정
    df.to_csv(filename+'.csv',encoding='utf-8-sig')   # DataFrame을 csv 파일로 저장
    print("Finish Crawling!")
        # driver.close()

    # 주석처리 된 부분은 아직 필요 없는 부분입니다.
    # print('----' + str(i) + ' 번째 페이지 -----')
    # list3 = []
    #
    # for title in titles:
    #     list = title.select_one(' td.td_article > div.board-list > div > a').text
    #     list2 = ''.join(list.split())
    #     list3.append(list2)
    #
    # list4_sr = pd.Series(list3)
    # print(list4_sr)
    #
    # # for a in range(1, 3):
    #     # driver.find_element_by_xpath(f'//*[@id="main-area"]/div[5]/table/tbody/tr[{a}]/td[1]/div[2]/div/a').click()
    #     # time.sleep(3)
    #     # driver.back()
    #     # time.sleep(2)
    #     # driver.switch_to.frame("cafe_main")


for i in range(1):  # 지금은 일단 1, 2페이지만 받아오게 설정했습니다.
    driver.get("https://cafe.naver.com/dogpalza")
    driver.implicitly_wait(3)

    driver.find_element_by_name('query').send_keys('로얄캐닌 사료')  # 로얄캐닌 사료를 입력하기
    driver.find_element_by_name("query").send_keys(Keys.ENTER)  # 로얄캐닌 사료 입력한걸 엔터클릭하기
    time.sleep(2)

    driver.switch_to.frame("cafe_main")

    if i < 2:
        driver.find_element_by_xpath(f'//*[@id="main-area"]/div[7]/a[{i}+1]').click()  # 다음페이지로 넘어가 주는 것 입니다.
        crawling()
