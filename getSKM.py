import os
from time import sleep
from secret import skm_token, skm_uuid, TIME_OUT
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

SKM_path = os.getcwd() + "/SKM.png"
HS_path = os.getcwd() + "./HS.png"

def getSKM():

    if skm_token == "" or skm_uuid == "":
        return False

    skm_url = "https://jsstm.jszwfw.gov.cn/jkmIndex.html?token={}&uuid={}".format(
        skm_token, skm_uuid)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(skm_url)
    sleep(3)
    try:
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.ID, "hs-layout")))
    except Exception as e:
        print(e)
        driver.quit()
        return False
    driver.save_screenshot(SKM_path)

    hs = driver.find_elements(By.ID, "hs-layout")[0]
    hs.click()
    sleep(2)

    try:
        hs_detail = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hs-detail")))
        hs_detail.click()
    except Exception as e:
        print(e)
        driver.quit()
        return False

    driver.save_screenshot(HS_path)

    driver.quit()
    return True
