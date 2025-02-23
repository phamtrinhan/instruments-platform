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

# __all__ = ["get_token", "get_authorization_header"]

OPERATION_SYSTEM = "ubuntu"

if platform.system() == "Darwin":
    OPERATION_SYSTEM = "macos"
elif platform.system() == "Windows":
    OPERATION_SYSTEM = "windows"
elif platform.system() == "Linux":
    OPERATION_SYSTEM = "linux"
CHROME_DRIVER_PATH = "%s/grapechain/libs/chromedriver/%s/chromedriver" % (
    os.getenv("HOME"), OPERATION_SYSTEM)


def sleep_and_wait(seconds: int):
    time.sleep(seconds)


def get_content(url, delay=0, headless=True):
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # this parameter tells Chrome that
    # it should be run without UI (Headless)
    chrome_service = service.Service(executable_path=CHROME_DRIVER_PATH)
    # initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options, service=chrome_service)

    driver.get(url)
    if delay > 0:
        sleep_and_wait(delay)
    return driver.find_element_by_xpath("//div[@id='json']").text
