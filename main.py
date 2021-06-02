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
import time
from validator_collection import validators, checkers


def mark_attendence(username, password, subject):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    tmain = 3000
        
    t1=time.perf_counter()                                          #current-time
    driver.implicitly_wait(45)
    driver.set_page_load_timeout(500)
    end=0
    while end==0:
            try:
                driver.get("https://ilizone.iul.ac.in/my/")     #Your moodle website address
                print("Working fine, opened ili login page!")
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
    driver.quit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        password = sys.argv[2]
        subject =  sys.argv[3]
    else:   
        print("You can also pass commandline arguments with AACS_ILI in this way: AACS_ILI.exe Username Password Subject_Code")
        print("")
        print("Optionally you can pass chrome window size and timeout of whole program(default=3000seconds) execution in commandline arguments with AACS_ILI in this way: AACS_ILI.exe Username Password Subject_Code 1920 1080 2500")
        print("")
        username = input("Enter in your username: ")
        password = getpass("Enter your password: ")
        subject =  input("Enter 1 ILI Subject Code(eg. CS311_A,CS309_B..., make sure your enter exactly like mentioned in ILI) OR You can enter the link of course page: ")
    mark_attendence(username, password,subject)