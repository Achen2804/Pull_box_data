from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json
from datetime import datetime
import os
def initialize_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver
def stamp_to_int(stamp):
    h, m, s = 0, 0, 0
    match_h = re.search(r'(\d+)h', stamp)
    match_m = re.search(r'(\d+)m', stamp)
    match_s = re.search(r'(\d+)s', stamp)
    if match_h: h = int(match_h.group(1))
    if match_m: m = int(match_m.group(1))
    if match_s: s = int(match_s.group(1))
    return h*3600 + m*60 + s

def get_pull_data(driver, url):
    driver.get(url)
    pull_button = driver.find_element(By.XPATH,"//button[.//path]")
    pull_button.click()
    value_box = driver.find_element(By.XPATH, '//span[svg[@alt="Coin"]]')
    pull_value = value_box.text
    print(f"Pull value: {pull_value}")

get_pull_data(initialize_driver(), "https://www.pullbox.gg/")