from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import json

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

def get_raffle_data(driver, url):
    driver.get(url)
    raffle_container = driver.find_elements(By.CSS_SELECTOR, '.p-6.bg-card.rounded-lg.border-2.border-border.hover\:border-primary\/50.transition-colors')
    raffle_types = ["hourly", "12hour", "24hour"]
    raffles = {rtype: [] for rtype in raffle_types}
    for i, item in enumerate(raffle_container):
        if i >= len(raffle_types):
            break

        time = item.find_element(By.XPATH, './div[2]/p[1]').text
        time = stamp_to_int(time)
        print(f"Raffle time in seconds: {time}")
        if time > 300:
            print("Raffle ends in more than 24 hours, skipping.")
            continue
        raffle_entries=(item.find_element(By.XPATH, './div[3]/div[1]/span[2]'))
        raffle_items=(item.find_element(By.XPATH, './div[1]/button/div[2]/p[1]'))
        raffle_value=(item.find_element(By.XPATH, './div[1]/button/div[2]/div[1]/p[1]'))
        raffle_type = raffle_types[i]
        raffles[raffle_type].append({
            'entry': raffle_entries.text,
            'item': raffle_items.text,
            'value': raffle_value.text})
    raffles = {k: v for k, v in raffles.items() if v}
    for rtype, data in raffles.items():
        with open(f"raffles/{rtype}.json", "w") as f:
            json.dump(data, f, indent=2)
    return raffles

data = get_raffle_data(initialize_driver(), 'https://www.pullbox.gg/limited-event/winter-wonderland/raffle')

