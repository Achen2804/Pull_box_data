from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    pull_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'size-full') and contains(@class,'rounded-l-sm') and contains(@class,'bg-stripes-muted') and .//*[name()='svg']]"
        ))
    )
    print(f"Pull button found")
    pull_button.highlighted = True
    pull_button.click()
    data_box = driver.find_element(
    By.CSS_SELECTOR,
    "div.pointer-events-auto.absolute.right-0.isolate.z-10.flex.h-full.transition-transform.duration-200.ease-out.translate-x-0"
)
    value_box = data_box.find_element(By.XPATH, '//span[.//img[@alt="Coin"]]')
    pull_value = value_box.text
    print(f"Pull value: {pull_value}")

    online_box = data_box.find_element(By.CLASS_NAME,"text-xs.font-normal.leading-none")
    online_box = online_box.find_element(By.TAG_NAME,"number-flow-react")
    online_value = online_box.text
    print(f"Online users: {online_value}")

    print("Pull value = ", float(pull_value)/float(online_value))
    if (datetime.now().minute >20 and datetime.now().minute <30) or (datetime.now().minute >50 and datetime.now().minute <=59):
        raise ValueError("Scrapped too early, will skip.")
    path = "data/data.json"
    try:
        if os.path.exists(path):
            with open(path, "w") as f:
                items = json.load(f)
                if not isinstance(items, list):
                    items = []
        else:
            items = []
        items.append({
            'pull_value': pull_value,
            'online_value': online_value,
            'ratio': float(pull_value)/float(online_value),
            'timestamp': datetime.now().isoformat()
        })
        with open(path, "w") as f:
            json.dump(items, f, indent=4)
    except json.JSONDecodeError:
        print("Error decoding JSON from data file.")
        

get_pull_data(initialize_driver(False), "https://www.pullbox.gg/")