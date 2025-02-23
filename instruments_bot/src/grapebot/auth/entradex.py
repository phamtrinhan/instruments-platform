import json
import os
import platform
import requests
import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from grapebot.storage import local

__all__ = ["get_token", "get_authorization_header"]

OPERATION_SYSTEM = "ubuntu"

if platform.system() == "Darwin":
    OPERATION_SYSTEM = "macos"
elif platform.system() == "Windows":
    OPERATION_SYSTEM = "windows"
elif platform.system() == "Linux":
    OPERATION_SYSTEM = "linux"

CREDENTIAL_PATH = "%s/grapechain/credentials/entradex.json" % (
    os.getenv("HOME"))

CHROME_DRIVER_PATH = "%s/grapechain/libs/chromedriver/%s/chromedriver" % (
    os.getenv("HOME"), OPERATION_SYSTEM)

if not local.check_file_exist(CHROME_DRIVER_PATH):
    local.create_folder_if_not_exist(
        '/'.join(CHROME_DRIVER_PATH.split("/")[:-1]))
    print("CHROMEDRIVE NOT FOUND. Need to be install at {}".format(CHROME_DRIVER_PATH))
    exit()

HEADERS = {}


def get_authorization_header():
    access_token = get_token()
    HEADERS["Authorization"] = access_token
    return HEADERS


def get_account_id():
    credential = load_credentials()
    return credential['account_id']


def get_token():
    credential = load_credentials()
    if "token" not in credential:
        token = authorize(credential["username"], credential["password"])
        credential["token"] = token
        with open(CREDENTIAL_PATH, 'w') as f:
            json.dump(credential, f)
    token: str = credential["token"]
    if not ping(token):
        token = authorize(credential["username"], credential["password"])
        credential["token"] = token
        with open(CREDENTIAL_PATH, 'w') as f:
            json.dump(credential, f)

    return token


def load_credentials():
    return json.load(open(CREDENTIAL_PATH))


def click_button(driver: webdriver, css_value: str):
    driver.find_element(By.CSS_SELECTOR, value=css_value).click()


def click_button_xpath(driver: webdriver, xpath_value: str):
    driver.find_element(By.XPATH, value=xpath_value).click()


def sleep_and_wait(seconds: int):
    time.sleep(seconds)


def authorize(username, password):
    # instance of Options class allows
    # us to configure Headless Chrome
    options = Options()

    # this parameter tells Chrome that
    # it should be run without UI (Headless)

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    chrome_service = service.Service(executable_path=CHROME_DRIVER_PATH)
    # initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options, service=chrome_service)

    driver.get("https://entradex.dnse.com.vn/dang-nhap?refPath=/")

    # We can also get some information
    # about page in browser.
    # So let's output webpage title into
    # terminal to be sure that the browser
    # is actually running.
    sleep_and_wait(1)

    sleep_and_wait(1)
    driver.find_element(
        By.XPATH, value="//input[@data-testid='input-login-username']").send_keys(username)
    driver.find_element(
        By.XPATH, value="//input[@data-testid='input-login-password']").send_keys(password)

    click_button_xpath(
        driver, xpath_value="//button[@data-testid='button-submit-login']")

    sleep_and_wait(1)
    driver.get("https://entradex.dnse.com.vn/")

    time.sleep(1)

    access_token = ""
    for request in driver.requests:
        if request.url == "https://services.entrade.com.vn/dnse-user-service/api/me":
            if "authorization" in request.headers:
                access_token = request.headers["authorization"]
    # close browser after our manipulations
    driver.close()
    driver.quit()
    return access_token


def ping(authorization_token: str):
    response = requests.get("https://services.entrade.com.vn/dnse-user-service/api/me",
                            headers={"authorization": authorization_token})
    if response.status_code != 200:
        return False
    return True
