import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

driver_path = "/Users/keitaro/Desktop/data_store/chromedriver/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(driver_path)

cns_username = "t20793km"
cns_password = "m522Keitaro"
url = "https://itclass.sfc.keio.ac.jp/typingtest/student/exercise?locale=ja#1"
driver.get(url)
username_form = driver.find_element_by_id("uid")
password_form = driver.find_element_by_id("pass")
login_button = driver.find_element_by_name("commit")
username_form.send_keys(cns_username)
password_form.send_keys(cns_password)
login_button.click()
go_test_button = driver.find_element_by_id("go-test-button")
go_test_button.click()
#start_text_button = driver.find_element_by_class_name("btn btn-xxl btn-reject")
start_text_button = driver.find_element_by_class_name("btn")
print(start_text_button)
print(dir(start_text_button))

#sleep(5)

#driver.close()



