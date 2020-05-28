from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re
import time

courses = []

ChromePath = r"C:\Users\nbink\Documents\GitHub\Banner-Scraper\chromedriver.exe"
driver = webdriver.Chrome(ChromePath)

textbox = ''

def initialize():
    global textbox
    website = driver.get('https://regssb.bannerxe.clemson.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search')

    dropDown = driver.find_element_by_xpath('''//*[@id="s2id_txt_term"]''').click()
    time.sleep(1)
    select = driver.find_element_by_xpath('''//*[@id="select2-results-1"]/li[3]''').click()
    time.sleep(1)
    Continue = driver.find_element_by_xpath('''//*[@id="term-go"]''').click()
    time.sleep(1)

def searchCourse(string):
    textbox = driver.find_element_by_xpath("""//*[@id="s2id_txt_subject"]""").click()
    time.sleep(1)
    textbox = driver.find_element_by_xpath("""//*[@id="s2id_autogen1"]""").send_keys(string) #Search for course
    time.sleep(1)
    textbox = driver.find_element_by_xpath("""//*[@id="s2id_autogen1"]""").send_keys(Keys.ENTER)
    Continue = driver.find_element_by_xpath('''//*[@id="search-go"]''').click() #Confirm course and continue
    time.sleep(1)

    showNumber = driver.find_element_by_xpath('''//*[@id="searchResultsTable"]/div[2]/div/div[3]/select''').click() #Show all 50
    Click50 = driver.find_element_by_xpath('''//*[@id="searchResultsTable"]/div[2]/div/div[3]/select/option[4]''').click()
    time.sleep(5) #Might take a second to load all 50, don't want to get ahead of ourselves here

    ClassCount = findAmountOfCourses()
    for i in range(ClassCount):
        course_info = getCourseInfo()
        print(course_info)
        goToNextCourse()

    raise Exception

def goToNextCourse():
    close = driver.find_element_by_xpath("""/html/body/div[176]/div[11]/div/button""").click()

    raise Exception

def findAmountOfCourses():
    column_count = len(driver.find_elements_by_xpath("//table[@id='table1']/tbody/tr"))
    return column_count

def getCourseInfo():
    section = driver.find_element_by_xpath('''//*[@id="table1"]/tbody/tr[1]/td[6]/a''').click()
    info = getMeetingTimes()
    return info

def getMeetingTimes():
    dateAndTime = driver.find_element_by_xpath("""//*[@id="facultyMeetingTimes"]/a""").click()

    title = driver.find_element_by_xpath("""//*[@id="202001.18320div"]/div""")
    raise Exception
    date = title.get_attribute("innerHTML")
    print(date)

    time.sleep(3)

    classTime = driver.find_element_by_xpath("""//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[1]""")
    classTime = classTime.get_attribute("innerHTML")

    classTime = re.sub(r'(?is)<span>', '', classTime) #remove spans
    classTime = re.sub(r'(?is)</span>', '', classTime)

    print(classTime.strip())

    extras = driver.find_element_by_xpath("""//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]""").text
    
    buildingAndRoom = parseExtras(extras)
    print(buildingAndRoom)
    return [date, classTime, buildingAndRoom]

def parseExtras(extras):
    items = extras.split("|")
    building = items[1]
    building = building.split()[0]
    print(building)

    room = items[2]
    room = room.split()[-1]
    
    return building + " " + room




def getCourseList():
    course = ''
    with open("CourseList.txt", 'r') as f:
        course = f.readline().rstrip()
        while course:
            courses.append(course)
            course = f.readline().rstrip()
    

getCourseList()
for i in courses: 
    initialize()
    searchCourse("CPSC")