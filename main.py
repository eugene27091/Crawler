from selenium import webdriver
from datetime import date
import pandas as pd
import time

options = webdriver.ChromeOptions()
# options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
driver = webdriver.Chrome(options=options)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}


content_list = []
review_title_list = []
review_content_list = []
product_list = []
productName_list = []
product_url = []

def getCategoryUrlList(main_url):
    driver.get(main_url)
    a_href = '//*[@id="__next"]/div[1]/div[1]/div[3]/div/div/main/div/div[4]/div/div/div[{}]/div/a'

    for i in range(1, 21):
        a_href_lists = driver.find_elements_by_xpath(a_href.format(i))
        for a_href_list in a_href_lists:
            product_list.append(a_href_list.get_attribute("href"))  # get_attribute href만 가져오기
    return product_list

def reviewCrawling(url):
    title_lists = []
    content_list = []
    date_list = []
    starRating_list = []
    info_breed_list = []
    info_age_list = []

    review_num_url = '//*[@id="__next"]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/span[2]'
    review_num = driver.find_element_by_xpath(review_num_url)
    reviewNum = review_num.text
    characters = "(,)"
    for x in range(len(characters)):
        reviewNum = reviewNum.replace(characters[x], "")
    print("리뷰 총 개수: ", reviewNum)
    totalPage = int(int(reviewNum) / 30)
    print("총 ", totalPage, " 페이지 입니다.")

    url = url + "/reviews?page={}"  # ex) https://dogpre.com/product/84863/reviews
    print("지금 상품은 ", url[19:32], "입니다.")

    for pageNum in range(totalPage):    # 리뷰가 30개 이하인 것 들은 range(1) 로 두어야함. 그리고 엑셀파일에서 리뷰 개수와 비교하여 null값 빼주기
        driver.get(url.format(pageNum))
        print("***************지금은 리뷰 ", pageNum, "페이지 입니다.***************")
        time.sleep(5)

        review_title_url = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[2]/main/div[4]/div[{}]/div[2]/div[1]/div/h3'
        review_content_url = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[2]/main/div[4]/div[{}]/div[2]/div[1]/div/div'
        review_date_url = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[2]/main/div[4]/div[{}]/div[1]/div/div[1]'
        dog_info_breed_url = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[2]/main/div[4]/div[{}]/div[1]/div/div[3]/span[1]'
        dog_info_age_url = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[2]/main/div[4]/div[{}]/div[1]/div/div[3]/span[2]'
        star_rate_url = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[2]/main/div[4]/div[{}]/div[1]/div/div[1]/span'

        for i in range(1, 31):
            review_titles = driver.find_elements_by_xpath(review_title_url.format(i))
            if bool(review_titles):
                for review_title in review_titles:
                    # print("***** 리뷰 제목 *****")
                    # print(review_title.text)
                    if "," not in review_title.text:
                        title_lists.extend(review_title.text.split(','))
                    else:
                        title_lists.append(review_title.text.replace(",", ""))
            else:
                title_lists.append("null")

            review_contents = driver.find_elements_by_xpath(review_content_url.format(i))
            for review_content in review_contents:
                # print("***** 리뷰 내용 *****")
                # print(review_content.text)
                content_list.append(review_content.text)

            review_dates = driver.find_elements_by_xpath(review_date_url.format(i))
            for review_date in review_dates:
                # print("***** 리뷰 날짜 *****")
                # print(review_date.text)
                date_list.extend(review_date.text.split(','))

            star_rates = driver.find_elements_by_xpath(star_rate_url.format(i))
            for star_rate in star_rates:
                # print("***** 별점 *****")
                # print(star_rate.get_attribute("aria-label"))
                starRating_list.append(star_rate.get_attribute("aria-label"))

            dog_info_breeds = driver.find_elements_by_xpath(dog_info_breed_url.format(i))
            for dog_info_breed in dog_info_breeds:
                # print("***** 강아지 정보 *****")
                # print(dog_info_breed.text)
                info_breed_list.extend(dog_info_breed.text.split(','))

            dog_info_ages = driver.find_elements_by_xpath(dog_info_age_url.format(i))
            if not bool(dog_info_ages):
                info_age_list.append("null")
            for dog_info_age in dog_info_ages:
                # print("***** 강아지 정보 *****")
                # print(dog_info_age.text)
                info_age_list.extend(dog_info_age.text.split(','))

    sample_lists = list(filter(None, content_list)) # 배열에 공백이 있다면 제거하기
    review_content_list = []

    for sample_list in sample_lists:    # 리뷰 내용을 가져와서 콤마(,)로 구분하기
        if sample_list != "2" and sample_list != "3" and sample_list != "4" and sample_list != "5" and sample_list != "6" and sample_list != "7":
            # print(sample_list)
            item_mod2 = sample_list.replace(",", " ")
            review_content_list.extend(item_mod2.split(','))

    return title_lists, review_content_list, date_list, starRating_list, info_breed_list, info_age_list

def getItemData(url):
    driver.get(url)
    product_name = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/h2')    # 상품명 받기
    productName = product_name.text # 상품명 받기
    print(productName)
    title_lists, review_content_list, date_list, starRating_list, info_breed_list, info_age_list = reviewCrawling(url)
    return {'item_name': productName, 'review_title': title_lists, 'review_content': review_content_list, 'review_date': date_list, 'review_star': starRating_list, 'dog_breed': info_breed_list, 'dog_age': info_age_list}

def getAllItemData():
    product_urls = getCategoryUrlList("https://dogpre.com/category/036?page=9&sortBy=CATEGORY_RANKING_SCORE_DESC")
    item_list = []
    for i in range(1,21): # 페이지에 모든 상품을 받기
        item_data = getItemData(product_urls[i])
        item_list.append(item_data)
    return item_list

def main():
    today = date.today()
    filename = f'dogPre{today.year}_{today.month}_{today.day}_page10_20'
    item_data_list = getAllItemData()
    main_list = []
    for item_data in item_data_list:
        main_list.append([item_data['item_name'], item_data['review_title'], item_data['review_content'], item_data['review_date'], item_data['review_star'], item_data['dog_breed'],item_data['dog_age']])

    df = pd.DataFrame(main_list)   # pd.DataFrame 생성
    df.columns = ['item_name', 'review_title', 'review_content', 'review_date', 'review_star', 'dog_breed', 'dog_age']   # columns 설정
    df.to_csv(filename+'.csv',encoding='utf-8-sig')   # DataFrame을 csv 파일로 저장
    print("Finish Crawling!")
    driver.close()

main()