from selenium import webdriver
import re
import pandas as pd
import os
from time import sleep
from selenium.webdriver.common.by import By

def saveBranchTables(args):

    driver = webdriver.Chrome('./chromedriver')
    url = f"https://www.kfcc.co.kr/gumgo/regulardisclosure.do?baseYear={args.year}&baseMonth={args.month}"
    driver.get(url)
    driver.maximize_window()
    sleep(2)

    if not os.path.exists('./data'):
        os.makedirs('./data')

    firstRound = True
    roundNum = 0
    withinRound = 0

    if args.start_page:
        for i in range((args.start_page-1)//10):
            nextRoundBtn = driver.find_element(By.CLASS_NAME, 'next')
            driver.execute_script("arguments[0].click();", nextRoundBtn)
            sleep(2)
            firstRound = False
            roundNum += 1
        
        withinRound = ((args.start_page -  1) % 10)
        if withinRound > 0:
            if not firstRound:
                pageBtn = driver.find_element(By.XPATH, f'//*[@id="gumgoList"]/div[2]/ul/li[{withinRound+3}]/a')
                driver.execute_script("arguments[0].click();", pageBtn)
                sleep(2)
            else:
                pageBtn = driver.find_element(By.XPATH, f'//*[@id="gumgoList"]/div[2]/ul/li[{withinRound+2}]/a')
                driver.execute_script("arguments[0].click();", pageBtn)
                sleep(2)
            # withinRound += 1

    while roundNum <= 12:
        # print(roundNum)
        for pageNum in range(withinRound, 10):
            if firstRound:
                if pageNum == 9:
                    firstRound = False
            else:
                pageNum += 1
            pageBtn = driver.find_element(By.XPATH, f'//*[@id="gumgoList"]/div[2]/ul/li[{pageNum+2}]/a')
            driver.execute_script("arguments[0].click();", pageBtn)
            sleep(2)
            lstItems = driver.find_elements(By.XPATH, f'//*[@id="gumgoList"]/div[1]/div/ul/li')
            for gumgoNum in range(2, len(lstItems) + 1):
                # driver.execute_script(f"window.scrollTo(0, {80*gumgoNum});")
                try:
                    row = driver.find_element(By.XPATH, f'//*[@id="gumgoList"]/div[1]/div/ul/li[{gumgoNum}]')
                    # driver.execute_script("arguments[0].scrollIntoView();", row)
                except:
                    sleep(3)
                    row = driver.find_element(By.XPATH, f'//*[@id="gumgoList"]/div[1]/div/ul/li[{gumgoNum}]')
                    # driver.execute_script("arguments[0].scrollIntoView();", row)
                gumgoBtn = row.find_element(By.XPATH, f'./div[1]/a')
                gumgoTel = row.find_element(By.XPATH, f'./div[4]').text
                gumgoTel = re.sub('-', '', gumgoTel)
                driver.execute_script("arguments[0].click();", gumgoBtn)
                sleep(2)
                try:
                    html = driver.page_source
                    f = open(f"./data/{gumgoTel}.html", 'w', encoding='utf-8-sig')
                    f.write(html)
                    f.close()
                    sleep(2)
                    driver.back()
                    sleep(2)
                except:
                    continue
            
            withinRound = 0

        nextRoundBtn = driver.find_element(By.XPATH, f'//*[@id="gumgoList"]/div[2]/ul/li[{pageNum+3}]/a')
        driver.execute_script("arguments[0].click();", nextRoundBtn)
        sleep(2)
        roundNum += 1
    sleep(2)
    driver.quit()