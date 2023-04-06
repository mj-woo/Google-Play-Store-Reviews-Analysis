import scrapy
import selenium
import re
from selenium import webdriver
from scrapy.selector import Selector
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By

class ReviewSpider(scrapy.Spider):
    name = "review"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps/details?id=com.locket.Locket"]

    def __init__(self):
        ##options=webdriver.ChromeOptions()
        options=webdriver.FirefoxOptions()
        ##options.add_argument("headless")
        options.add_argument("-headless")
        #desired_capabilities=options.to_capabilities
        ##desired_capabilities={'chromeOptions':{'args':['--disable-extensions']}}
        ##self.driver=webdriver.Chrome(executable_path='C:\chromedriver.exe',desired_capabilities=desired_capabilities)
        self.driver=webdriver.Firefox(executable_path='C:/geckodriver-v0.32.2-win-aarch64 (1)/gechodriver.exe')

    def parse(self, response):
        self.driver.get('https://play.google.com/store/apps/details?id=com.locket.Locket')

        SCROLL_PAUSE_TIME = 7
 
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        sleep(SCROLL_PAUSE_TIME)
    
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)
        
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        sleep(2)
        self.driver.execute_script("window.scrollBy(0,-250)")
        sleep(2)
        # click the show all results button
        view_all=self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button/span')
        view_all.click()
        sleep(6)

        names=[]
        reviews=[]
        dates=[]
        ratings=[]
        agreed=[]
        terminate=0
        prev=-1

        # while True:
        for i in range(450):
            last_comment=self.driver.find_elements(By.CLASS_NAME,value='h3YV2d')[-1]
            past_comment=last_comment
            self.driver.execute_script("arguments[0].scrollIntoView();",past_comment)
            sleep(7)

        scrapy_selector=Selector(text=self.driver.page_source)
        names_list=scrapy_selector.css(".X5PpBb::text").extract()
        reviews_list=scrapy_selector.css(".h3YV2d::text").extract()
        ratings_list=scrapy_selector.css(".iXRFPc::attr(aria-label)").extract()
        agreed_list=scrapy_selector.css(".AJTPZc::text").extract()
        date_list=scrapy_selector.css(".bp9Aid::text").extract()
            

        # for(name,review,rating,agreed_text,date) in zip(names_list,reviews_list,ratings_list,agreed_list,date_list):
        #     # if review not in reviews:
        #     names.append(name)
        #     reviews.append(review)
        #     dates.append(date)
        #     ratings.append(rating)
        #     agreed.append(agreed_text)
        #     print("prev:", prev)
        #     flag=len(reviews)
        #     prev=flag
        #     print(prev)
        #     print('leng ', len(names_list))
        #     if flag==9000:
        #         terminate=1
        #         break
            # data={'names':names,
            #     'reviews':reviews,
            #     'ratings':ratings,
            #     'agreed':agreed,
            #     'date':dates,
            # }

            # if terminate==1:
        self.driver.close()
                # break


            # self.driver.execute_script("arguments[0].scrollIntoView();",last_comment)
            # sleep(5)

        data={'names':names_list,
                'reviews':reviews_list,
                'ratings':ratings_list,
                # 'agreed':agreed_list,
                'date':date_list,
        }

        data2={'agreed': agreed_list}

        df=pd.DataFrame(data)
        df.to_csv('locketwidget_review.csv')

        # while True:
        #     # scrapy_selector=Selector(text=self.driver.page_source)
        #     last_comment=self.driver.find_elements(By.CLASS_NAME,value='h3YV2d')[-1]
        #     self.driver.execute_script("arguments[0].scrollIntoView();",last_comment) 
        #     sleep(1)
        # if terminate==1:
        #     break

        # self.driver.execute_script("arguments[0].scrollIntoView();",last_comment)
        # sleep(1)