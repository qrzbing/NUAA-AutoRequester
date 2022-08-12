import datetime
import getSKM
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from secret import username, password, leave_school_reason, SKM_path, XCM_path, HS_path
from selenium.webdriver.chrome.options import Options

flagSKM = getSKM.getSKM()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://ehall.nuaa.edu.cn/infoplus/form/YQFKXSFXLSCX_CS/start?theme=nuaa_new"
driver.get(url)

TIME_OUT = 20

def login_in(username, password):

    driver.find_elements(By.ID, "username")[0].send_keys(username)
    driver.find_elements(By.ID, "password")[0].send_keys(password)

    loginButton = driver.find_elements(By.ID, "login_submit")[0]
    loginButton.click()


def prev_start():
    try:
        prev_start_btn = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.ID, "preview_start_button")))
        prev_start_btn.click()
    except Exception as e:
        print(e)
        driver.quit()
        exit(0)


def fill_form():
    def select_date(from_date="", to_date=""):
        if from_date == "":
            today = datetime.date.today()
            from_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            to_date = from_date

        calendar_start = driver.find_elements(By.NAME, "fieldCXRQ")[0]
        calendar_start.clear()
        calendar_start.send_keys(from_date)
        sleep(1)

        calendar_end = driver.find_elements(By.NAME, "fieldJSSJ")[0]
        calendar_end.clear()
        calendar_end.send_keys(to_date)
        sleep(1)

        calendar_start.click()
        calendar_end.click()

    def select_time(from_time="00:00", to_time="23:59"):
        time_start = driver.find_elements(By.NAME, "fieldCXSJFROM")[0]
        time_start.clear()
        time_start.send_keys(from_time)
        sleep(1)

        time_end = driver.find_elements(By.NAME, "fieldCXSJTO")[0]
        time_end.clear()
        time_end.send_keys(to_time)
        sleep(1)

    try:
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.ID, "fieldXSLX-0")))
    except Exception as e:
        print(e)
        driver.quit()
        exit(0)

    # 上传三码
    upload_SKM = driver.find_elements(By.NAME, 'qqfile')[0]
    upload_SKM.send_keys(SKM_path if not flagSKM else getSKM.SKM_path)

    upload_XCM = driver.find_elements(By.NAME, 'qqfile')[1]
    upload_XCM.send_keys(XCM_path)

    upload_HS = driver.find_elements(By.NAME, 'qqfile')[2]
    upload_HS.send_keys(HS_path if not flagSKM else getSKM.HS_path)

    # 选择进出日期
    # format: YYYY-MM-DD
    # 默认申请明天的出校
    today = datetime.date.today()
    from_date = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    to_date = from_date
    select_date(from_date, to_date)

    # 所在校区
    # - 1：明故宫校区
    # - 2：将军路校区
    # - 3：天目湖校区
    school_path_select = Select(driver.find_elements(By.NAME, "fieldASZXQ")[0])
    school_path_select.select_by_value("2")

    # 选择进出时间
    # By default, from 00:00 to 23:55
    select_time()

    # 学生类型
    sleep_input = driver.find_elements(By.ID, "fieldXSLX-0")[0]
    sleep_input.click()

    reason = driver.find_elements(By.NAME, "fieldCXSY")[0]
    reason.clear()
    reason.send_keys(leave_school_reason)

    category = driver.find_elements(By.ID, "V1_CTRL107")[0]
    category.click()

    leaveNJ = driver.find_elements(By.NAME, "fieldAcxxc")[1]
    leaveNJ.click()

    returnSchool = driver.find_elements(By.NAME, "fieldAds")[0]
    returnSchool.click()

    confirm = driver.find_elements(By.NAME, "fieldCN")[0]
    confirm.click()

    sleep(5)

    submit_button = driver.find_elements(By.ID, 'form_holder')[0].find_elements(
        By.CLASS_NAME, "command_button_content")[0]
    submit_button.click()



def main():
    login_in(username, password)
    sleep(5)
    prev_start()
    fill_form()
    try:
        text_ok = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form_do_action_error")))
        if text_ok.text == u"您好，您出行申请已提交，请耐心等待审核。":
            print("提交成功")
    except Exception as e:
        print(e)
        driver.quit()
        exit(0)
    driver.quit()

if __name__ == "__main__":
    main()


