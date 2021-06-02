from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from getpass import getpass
import contextlib
import urllib3
import os
import sys
import time,datetime
from validator_collection import validators, checkers
import json

def mark_attendence(username, password, subject):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    tmain = 900    
    t1=time.perf_counter()                                          #current-time
    driver.implicitly_wait(45)
    driver.set_page_load_timeout(240)
    end=0
    while end==0:
            try:
                driver.get("https://ilizone.iul.ac.in/my/")     #Your moodle website address
                t2=time.perf_counter()                          #time-now
                if t2-t1 > tmain:                               #comment this 'if' you don't need timeout for your works...
                    driver.quit()                           #
                if not driver.find_elements_by_xpath("//span[@class='userbutton']"):    #For checking if logged in or not
                    username_textbox = driver.find_element_by_id("username")
                    username_textbox.send_keys(username)
                    password_textbox = driver.find_element_by_id("password")
                    password_textbox.send_keys(password)
                    login_button = driver.find_element_by_id("loginbtn")
                    login_button.submit()
                if(checkers.is_url(subject)):
                    driver.get(subject)
                    driver.find_element_by_link_text("Attendance").click()
                    driver.find_element_by_link_text("Submit attendance").click()
                    driver.find_element_by_xpath("//span[text()='Present']").click()
                    driver.find_element_by_xpath("//input[@value='Save changes']").click()
                    end=1
                else:
                    driver.find_element_by_link_text(subject).click()
                    driver.find_element_by_link_text("Attendance").click()
                    driver.find_element_by_link_text("Submit attendance").click()
                    #wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Present']"))).click()
                    driver.find_element_by_xpath("//span[text()='Present']").click()
                    driver.find_element_by_xpath("//input[@value='Save changes']").click()
                    end=1
            except NoSuchElementException:
                    end=0
            except TimeoutException:
                    end=0
            except WebDriverException:
                    end=0
    return

username = []
password = []
course = []
timetables = []
total = []
urls = []

if __name__ == '__main__':
    with open("users.json") as jsonFile1: #Import users data from users.json to lists
        users = json.load(jsonFile1)
        total_users = users["Total"]
        for i in range(total_users):
            username.append(users[f"{i}"]["username"])
            password.append(users[f"{i}"]["password"])
            course.append(users[f"{i}"]["course"])
while True:    
        now = datetime.datetime.now()
        day = now.strftime("%A")
        if day == "Sunday":
            sys.exit()
        with open("timetable.json") as jsonFile2: #Import timetable of every user in a list
            timetable = json.load(jsonFile2)
            for i in range(len(course)):
                timetables.append(timetable[f"{course[i]}"][f"{day}"])  #Importing Today timetable
                total.append(int(timetables[i]["Total"]))   #Importing Total number of periods today
                for j in range(total[i]):
                    if str(timetables[i][f"{j}"]["at"]) == now.strftime("%H:%M"): #If time matches with at variable
                        urls.append(timetables[i][f"{j}"]["url"])   #Save the url for marking the attendence
        
        for i in range(len(urls)):
            mark_attendence(username[i], password[i],urls[i]) #Marking attendence
        urls.clear()
        now6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
        if now >= now6pm:
            sys.exit()
