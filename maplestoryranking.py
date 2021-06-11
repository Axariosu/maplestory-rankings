import json, requests
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html

# link="https://maplestory.nexon.net/rankings/overall-ranking/legendary?page_index=13957170&rebootIndex=0"

def main(): 
    # k=13957170 is the start of level 35 characters as of 27 May 2021
    # k=13992460 as of 10 June 2021
    # k=33483250 last page
    start_index, end_index = 13992460, 33483250

    # dangerous line
    f = open('names.txt', "w+")
    f.write(str(start_index))

    link='https://maplestory.nexon.net/rankings/overall-ranking/legendary?page_index=' + str(start_index) + '&rebootIndex=0'
    # open selenium browser, reduce noise
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    for i in range(start_index, end_index, 5): 
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # get raw text from maplestory leaderboard rankings
        text = soup.get_text()
        start_text = "NameWorldJobLevel/Move"
        start = text.find(start_text)
        end_text = "<>"
        end = text.find(end_text)
        raw_text = text[start+len(start_text):end-len(end_text)]
        
        # returns alpha char names only 
        l = [x for x in re.split(r'(\d+)', raw_text) if x.isalpha()]
        print(l)
        for name in l: 
            f.write(name + "\n")
        # advance page
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-rank-list__arrow.c-rank-list__arrow--right")))
        element.click()

        # runtime per loop, safety feature? 
        time.sleep(0.075)

    f.write(str(end_index))
    f.close()
    print("done")

if __name__ == "__main__": 
    main()