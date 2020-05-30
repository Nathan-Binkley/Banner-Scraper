from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re
import time

'''
TODO: 
After it completes, go to next search term
'''



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

    # print(len(ClassElements))
    

    while True:
        ClassElements = driver.find_elements_by_class_name("section-details-link")
        for i in ClassElements:
            course_info = ''
            try:
                course_info = getCourseInfo(i)
                print(course_info)
            except:
                print("NO COURSE INFO")
            time.sleep(2)
            try:
                goToNextCourse()
            except:
                pass
            time.sleep(2)
        try: 
            gotoNextPage = driver.find_element_by_class_name("paging-control.next.ltr.enabled").click()
            time.sleep(10)
        except:
            break
    raise Exception


def goToNextCourse():
    close = driver.find_element_by_class_name("""ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only.primary-button.small-button""").click() #Exit current course (Close button)
    

def getCourseInfo(course):
    # print(course)
    section = course.click() #Clicked on the section
    time.sleep(1)
    dateAndTime = getDateAndTime()
    capacity = getCapacity()
    dateAndTime.append(capacity)
    allInfo = dateAndTime
    return allInfo

    

def getCapacity():
    info = driver.find_element_by_id("enrollmentInfo").click()
    time.sleep(1)
    details = driver.find_element_by_id("classDetailsContentDetailsDiv").get_attribute("innerHTML")
    return getMaxCapacity(details)
    
def getMaxCapacity(details):
    
    items = details.split("\n")
    
    details = items[3]
    details = re.sub('<[^>]+>', '', details)
    splitDeets = details.split()
    details = []
    for i in splitDeets:
        if i:
            details.append(i)

    return details

def getDateAndTime():  
    classDAT = driver.find_element_by_id("facultyMeetingTimes").click()
    time.sleep(1)
    timeAndLoc = driver.find_element_by_class_name("right").get_attribute("innerHTML")

    timeAndLoc = re.sub(r'(?is)<span>', '', timeAndLoc)
    timeAndLoc = re.sub(r'(?is)</span>', '', timeAndLoc)
    timeOfClass, loc = timeAndLoc.split("</div>",1)
    timeOfClass = re.sub(r'(?is)<div>', '', timeOfClass)
    loc = re.sub(r'(?is)<div>', '', loc)
    loc = re.sub(r'(?is)</div>', '', loc)

    locInfo = loc.split("|")
    loc = locInfo[1].split()[0] + " " + locInfo[2].split()[-1]
    
    
    daysOfWeek = driver.find_element_by_class_name("ui-pillbox")
    daysOfWeek = daysOfWeek.get_attribute("title")
    daysOfWeek = daysOfWeek.split()[-1]

    return [daysOfWeek, timeOfClass, loc]


def parseExtras(extras):
    items = extras.split("|")
    building = items[1]
    building = building.split()[0]
    

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