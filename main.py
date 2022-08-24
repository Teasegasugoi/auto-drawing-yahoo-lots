import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import signal
import time


# Yahoo!JAPAN HOME URL
YAHOO_HOME_URL = "https://www.yahoo.co.jp/"

# Yahoo!JAPAN LOGIN URL
YAHOO_LOGIN_URL = "https://login.yahoo.co.jp/config/login"


def main():
    # .envファイルの内容を読み込む
    load_dotenv()

    # Chrome の起動オプションを設定する
    options = webdriver.ChromeOptions()

    try:
        # 1. ブラウザの新規ウィンドウを開く
        driver = webdriver.Chrome(options=options)
        # 2. Yahoo JAPAN にアクセス
        driver.get(YAHOO_HOME_URL)
        # 3. ズバトク
        driver.find_element(By.XPATH, "//a[@aria-label='ズバトクへ遷移する']").click()

        # ログイン
        login(driver)

    except:
        driver.quit()

    else:
        os.kill(driver.service.process.pid,signal.SIGTERM)

# ログイン
def login(driver):
    try:
        login_link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mhLogin"))
        )
        login_link_element.click()
        mail_or_phone_element = driver.find_element(By.ID, "username")
        mail_or_phone_element.send_keys(os.environ['PHONE_NUMBER'])
        driver.find_element(By.ID, "btnNext").click()
        # 確認コード入力
        print("届いた確認コードを入力してください")
        auth_code = int(input("> "))
        code_element = driver.find_element(By.ID, "code")
        code_element.send_keys(auth_code)
        driver.find_element(By.ID, "btnSubmit").click()
        time.sleep(2)
        if (driver.current_url == YAHOO_LOGIN_URL):
            print("確認コードが違います")
            raise Exception
    except:
        print("ログインに失敗しました")
        raise Exception

if __name__ == "__main__":
    main()