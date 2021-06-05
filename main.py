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
import os,sys
import time,datetime
from validator_collection import checkers
import json

def mark_attendence(username, password, link):
    global marked
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    tmain = 700    
    t1=time.perf_counter()                                          #current-time
    driver.implicitly_wait(45)
    driver.set_page_load_timeout(100)
    end=0
    while end==0:
        try:
            driver.get("https://ilizone.iul.ac.in/my/")     #Your moodle website address
            t2=time.perf_counter()                          #time-now
            if t2-t1 > tmain:                               #comment this if you don't need timeout for your works...
                end=1                         
            if driver.find_elements_by_xpath("//span[@class='login']"):    #For checking if logged in or not
                username_textbox = driver.find_element_by_id("username")
                username_textbox.send_keys(username)
                password_textbox = driver.find_element_by_id("password")
                password_textbox.send_keys(password)
                login_button = driver.find_element_by_id("loginbtn")
                login_button.submit()
            if(checkers.is_url(link)):
                driver.get(link)
                driver.find_element_by_link_text("Attendance").click()
                driver.find_element_by_link_text("Submit attendance").click()
                driver.find_element_by_xpath("//span[text()='Present']").click()
                driver.find_element_by_xpath("//input[@value='Save changes']").click()
                marked=True
                end=1
            else:
                end=1
            # else:
            #     driver.find_element_by_link_text(link).click()
            #     driver.find_element_by_link_text("Attendance").click()
            #     driver.find_element_by_link_text("Submit attendance").click()
            #     #wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Present']"))).click()
            #     driver.find_element_by_xpath("//span[text()='Present']").click()
            #     driver.find_element_by_xpath("//input[@value='Save changes']").click()
            #     end=1
        except NoSuchElementException:
                end=0
        except TimeoutException:
                end=0
        except WebDriverException:
                end=0
    driver.quit()
    return

username = []
password = []
course = []
timetables = []
total = []
urls = []
saved_timetable = False
marked = False

if __name__ == '__main__':
    print("Program loaded successfully")
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
            os._exit(0)
        with open("timetable.json") as jsonFile2: #Import whole timetable of all courses
            timetable = json.load(jsonFile2)
            for i in range(len(username)):  #Running n number of times for all users
                timetables.append(timetable[f"{course[i]}"][f"{day}"])  #Importing Today timetable
                urls.append("none")
                total.append(int(timetables[i]["Total"]))   #Importing Total number of periods today
                if int(timetables[i]["Total"]) == 0:
                    continue
                else:
                    for j in range(total[i]):
                        if str(timetables[i][f"{j}"]["at"]) == now.strftime("%H:%M"): #If time matches with at variable
                            urls[i] = (timetables[i][f"{j}"]["url"])   #Save the url for marking the attendence

        if saved_timetable == False:
            for x in range(len(username)):      #Changing 'at' key and values to "marked" for saving if attendence is marked or not
                for y in range(total[x]):
                    timetables[x][f"{y}"]["marked"] = timetables[x][f"{y}"].pop("at")
                    timetables[x][f"{y}"]["marked"] = "no"
            with open('marked.json', 'w') as fp:
                json.dump(timetables, fp, indent=4, sort_keys=True)
                saved_timetable=True

        start = time.time()
        for i in range(len(username)):
            if urls[i] == 'none':
                continue
            else:
                mark_attendence(username[i], password[i],urls[i]) #Marking attendence
                if marked == True:
                    with open("marked.json", 'r') as jsonFile3: #Import marked.json
                        marked = json.load(jsonFile3)
                        for j in range(total[i]):
                            if urls[i] == marked[i][f"{j}"]['url']:
                                marked[i][f"{j}"]["marked"] = "yes" #Writing marked.json with attendence output
                        with open("marked.json", 'w') as jsonFile4:
                            json.dump(marked,jsonFile4, indent=4, sort_keys=True)
                    marked=False
        end = time.time()
        timetaken = int(end-start)
        if timetaken < 60:                    #If mark attendence job is done before 1min, this will compensate the time so that next loop only runs at 1 minute difference anyhow
            time.sleep(60-timetaken)                #This is done so that it doesn't run the loop at the same minute again and then just keep trying to mark attendence because there is currently no detection placed to detect if attendence is marked or not.

        urls.clear()
        total.clear()
        timetables.clear()

        now6pm = now.replace(hour=18, minute=00, second=0, microsecond=0)
        if now >= now6pm:
            print("Program completed its work for today and now exiting.")
            os._exit(0)
