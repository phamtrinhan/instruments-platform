import requests
import logging
import platform
from subprocess import PIPE, run
from datetime import datetime as dtime
from datetime import date
import os
from pathlib import Path
import wget
import shutil
from zipfile import ZipFile
import json
from grapebot import telegram
from grapebot import utils

import time
today = date.today()
today_in_ymd = dtime.today().strftime('%Y-%m-%d')
TEMP_PATH = f"{os.getenv('HOME')}/grapechain/env_temp"


def create_folder_if_not_exist(path):
    temp_path = path.split('/')
    if temp_path[-1].find('.') > -1:
        path = '/'.join(temp_path[:-1])
    if not os.path.exists(path):
        os.makedirs(path)


def save_object_to_file(data, source, file_name=today_in_ymd, path=''):
    if source != "":

        json_string = json.dumps(data, indent=4)
        # today_ymd = utils.today_in_ymd()

        storing_path = "{}/grapechain/data/".format(os.getenv("HOME")).format(
            **locals(), **globals()) if (path == '') else path.format(
            **locals(), **globals())
        create_folder_if_not_exist(storing_path)
        #
        with open(storing_path, 'w') as output_stream:
            output_stream.write(json_string)
        return storing_path
    else:
        raise Exception('Error')


def check_file_exist(file_path):
    return Path(file_path).is_file()


def get_chrome_version(ver):
    return '.'.join(ver.split(".")[:3])


def get_chrome_topversion(ver):
    return ver.split(".")[0]


def compare_chrome_version(first, second):
    return '.'.join(first.split('.')[:3]) == '.'.join(second.split('.')[:3])


def spcommand(command):
    logger.info("Run command: " + str(command))
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True,
                 shell=True)
    return result.stdout.replace("\n", "")


def check_driver_n_chrome(OPERATION_SYSTEM):
    if OPERATION_SYSTEM not in ["linux", "macos"]:
        raise Exception("Operation not support")
    if OPERATION_SYSTEM == "macos":
        CHROME_VERSION = spcommand(
            "echo $(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | awk '{print $3}')")
    else:
        CHROME_VERSION = spcommand(
            "echo $(chrome --version | awk '{print $5}')")
    CHROME_DRIVER_VERSION = spcommand(
        f"echo $({os_path}/grapechain/libs/chromedriver/"+OPERATION_SYSTEM+"/chromedriver --version | awk " + "'{print $2}')")

    if not compare_chrome_version(CHROME_VERSION, CHROME_DRIVER_VERSION):
        logger.critical(
            "Chrome version: " + '.'.join(CHROME_VERSION.split('.')[:3]))
        logger.critical("Chrome driver version: " + '.'.join(
            CHROME_DRIVER_VERSION.split('.')[:3]))

    return (CHROME_VERSION, CHROME_DRIVER_VERSION,
            compare_chrome_version(chrome_version, CHROME_DRIVER_VERSION))


# $(/Users/binhot/grapechain/libs/chromedriver/macos/chromedriver --version
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

logger = logging.getLogger("gc_env")
if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
os_path = os.getenv("HOME")

logger.info(f"Home path: {os_path}")
logger.info(f"Creating path if not exist")
create_folder_if_not_exist(f"{TEMP_PATH}/chromedriver")
create_folder_if_not_exist(f"{os_path}/grapechain/total/")

create_folder_if_not_exist(f"{os_path}/grapechain/total/daily/")
logger.info("[-] Start testing system")

OPERATION_SYSTEM = "ubuntu"
if platform.system() == "Darwin":
    OPERATION_SYSTEM = "macos"
elif platform.system() == "Windows":
    OPERATION_SYSTEM = "windows"
elif platform.system() == "Linux":
    OPERATION_SYSTEM = "linux"
try:

    if OPERATION_SYSTEM not in ["linux", "macos"]:
        raise Exception("Operation not support")
    if OPERATION_SYSTEM == "macos":
        chrome_version = spcommand(
            "echo $(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | awk '{print $3}')")
    else:
        chrome_version = spcommand(
            "echo $(chrome --version | awk '{print $5}')")

    if chrome_version == "":
        # if OPERATION_SYSTEM == "linux":
        #     spcommand("chmod +x chrome_install.sh")
        #     spcommand("./chrome_install.sh")
        raise Exception("Google chrome didn't install")
    create_folder_if_not_exist(
        f"{os_path}/grapechain/libs/chromedriver/{OPERATION_SYSTEM}/")
    CHROME_DRIVER_VERSION = spcommand(
        f"echo $({os_path}/grapechain/libs/chromedriver/{OPERATION_SYSTEM}/chromedriver --version | awk " + "'{print $2}')")
    logger.info(f"GOOGLE CHROME VERSION EX: {chrome_version}")
    logger.info(f"CHROME DRIVER VERSION EX: {CHROME_DRIVER_VERSION}")
    if not compare_chrome_version(chrome_version, CHROME_DRIVER_VERSION):
        logger.critical(
            "Chrome version: " + '.'.join(chrome_version.split('.')[:3]))
        logger.critical("Chrome driver version: " + '.'.join(
            CHROME_DRIVER_VERSION.split('.')[:3]))
        logger.critical(f"Google Chrome or Chrome Driver need to be upgraded")
        # raise Exception("Version chromedriver and google-chrome not match")
        cft_requests = requests.get(
            f"https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json").text
        cft_requests = json.loads(cft_requests)
        latest_version = cft_requests[
            'channels']['Stable']['version']
        logger.info(f"Latest version: {latest_version}")
        driver_type = ""
        if OPERATION_SYSTEM == "macos":
            if platform.machine() == "arm64":
                driver_type = "mac_arm64"
            else:
                driver_type = "mac64"
        elif OPERATION_SYSTEM == "linux":
            driver_type = "linux64"
        CHROME_SAVE_PATH = f"{TEMP_PATH}/chromedriver/chromedriver_latest.zip"
        for file in os.scandir(f"{TEMP_PATH}/chromedriver/"):
            os.remove(file.path)
        logger.info(f"Downloaded latest version: {latest_version}")
        filtered_drivers = [item for item in cft_requests['channels']['Stable']
                            ['downloads']['chromedriver'] if item['platform'] == driver_type]
        DOWNLOAD_CHROMEDRIVER_URL = filtered_drivers[0]['url']
        logger.info(f"Download file from {DOWNLOAD_CHROMEDRIVER_URL}")
        wget.download(DOWNLOAD_CHROMEDRIVER_URL, CHROME_SAVE_PATH)
        zf = ZipFile(CHROME_SAVE_PATH, 'r')
        zf.extractall(f"{TEMP_PATH}/chromedriver/")
        zf.close()

        shutil.copy(f"{TEMP_PATH}/chromedriver/chromedriver-{driver_type}/chromedriver",
                    f"{os_path}/grapechain/libs/chromedriver/{OPERATION_SYSTEM}/")
        spcommand(
            f"chmod +x {os_path}/grapechain/libs/chromedriver/{OPERATION_SYSTEM}/chromedriver")
        logger.info("Upgrade Chrome Driver complete")
        CHROME_VERSION, CHROME_DRIVER_VERSION, CHROME_N_DRIVER_OK = check_driver_n_chrome(
            OPERATION_SYSTEM)
        if not CHROME_N_DRIVER_OK:
            raise Exception("Can't do upgrade. Please do it manually")
    logger.info(f"[{'-' * 30}]")
    logger.info("Try to import Selenium")
    from seleniumwire import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome import service
    from selenium.webdriver.common.by import By

    logger.info("Testing Selenium")
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # this parameter tells Chrome that
    # it should be run without UI (Headless)
    chrome_service = service.Service(
        executable_path=f"{os_path}/grapechain/libs/chromedriver/{OPERATION_SYSTEM}/chromedriver")
    # initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options, service=chrome_service)

    driver.get("https://www.google.com/")
    js = '''
        let callback = arguments[0];
        let xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://www.google.com/', true);
        xhr.onload = function () {
            if (this.readyState === 4) {
                callback(this.status);
            }
        };
        xhr.onerror = function (err) {
            console.log(err);
            callback('error');
        };
        xhr.send(null);
    '''

    status_code = driver.execute_async_script(js)
    # print('Status ', status_code)  # 200
    if status_code in [200, 301, 302]:
        logger.info("Seleium OK")
    else:
        raise Exception("Selenium failed")
    # time.sleep()
    driver.close()
    driver.quit()
    logger.info("Testing system success")
    logger.info("[-] SYSTEM ENVIRONMENT: PASSED")

    telegram.send_message(f"Today: {utils.today_in_ymd()} ")
    telegram.send_message("[-] SYSTEM ENVIRONMENT: PASSED")
    telegram.send_message("[-] PRODUCTION ENVIRONMENT: PASSED")
    telegram.send_message("[-] API VERSION: NOT PASSED")
    telegram.send_message("[-] HI TELEGRAM: PING PONG")
    telegram.send_message("[✓] PASSED")

except Exception as e:
    logger.error("Testing system failed")
    logger.error(e)
