from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


ChromePath = r"C:\Users\nbink\Documents\GitHub\Banner-Scraper\chromedriver.exe"
driver = webdriver.Chrome(ChromePath)

website = driver.get('https://regssb.bannerxe.clemson.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search')

dropDown = driver.find_element_by_xpath('''//*[@id="s2id_txt_term"]''').click()
time.sleep(1)
select = driver.find_element_by_xpath('''//*[@id="select2-results-1"]/li[3]''').click()
time.sleep(1)
Continue = driver.find_element_by_xpath('''//*[@id="term-go"]''').click()