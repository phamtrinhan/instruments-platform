from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
import ssl
import json
import os
import platform
import requests

from grapebot.storage import local

__all__ = ["get_token", "get_authorization_header"]

OPERATION_SYSTEM = "ubuntu"

if platform.system() == "Darwin":
    OPERATION_SYSTEM = "macos"
elif platform.system() == "Windows":
    OPERATION_SYSTEM = "windows"
elif platform.system() == "Linux":
    OPERATION_SYSTEM = "linux"

CREDENTIAL_PATH = "%s/grapechain/credentials/tcbs.json" % (os.getenv("HOME"))

CHROME_DRIVER_PATH = "%s/grapechain/libs/chromedriver/%s/chromedriver" % (
    os.getenv("HOME"),
    OPERATION_SYSTEM,
)

if not local.check_file_exist(CHROME_DRIVER_PATH):
    local.create_folder_if_not_exist("/".join(CHROME_DRIVER_PATH.split("/")[:-1]))
    print("CHROMEDRIVE NOT FOUND. Need to be install at {}".format(CHROME_DRIVER_PATH))
    exit()


def get_authorization_header():
    HEADERS = {}

    access_token = get_token()
    HEADERS["Authorization"] = "Bearer " + access_token
    return HEADERS


def get_account_id():
    credential = load_credentials()
    return credential["account_id"]


def get_token():
    credential = load_credentials()
    if "token" not in credential:
        token = authorize(credential["username"], credential["password"])
        credential["token"] = token
        with open(CREDENTIAL_PATH, "w") as f:
            json.dump(credential, f)
    token: str = credential["token"]
    if not ping(token):
        token = authorize(credential["username"], credential["password"])
        credential["token"] = token
        with open(CREDENTIAL_PATH, "w") as f:
            json.dump(credential, f)

    return token


def load_credentials():
    return json.load(open(CREDENTIAL_PATH))


class SSLAdapter(HTTPAdapter):
    """An HTTP adapter that uses a custom SSL context."""

    def __init__(self, ssl_context):
        self.ssl_context = ssl_context
        super().__init__()

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def authorize(username, password):
    url = "https://apipub.tcbs.com.vn/authen/v1/login"

    payload = json.dumps(
        {
            "username": username,
            "password": password,
            "device_info": json.dumps(
                {
                    "os.name": "Macintosh",
                    "os.version": 10.157,
                    "browser.name": "Chrome",
                    "browser.version": 122,
                    "navigator.userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "navigator.appVersion": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "navigator.platform": "MacIntel",
                    "navigator.vendor": "Google Inc.",
                }
            ),
        }
    )
    headers = {"Content-Type": "application/json"}

    # Create a custom SSL context (this is where you'd need to define your SSL options)
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    # Example, might not work as intended

    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.options |= 0x4

    session = requests.Session()
    adapter = SSLAdapter(ssl_context)
    session.mount("https://", adapter)

    try:
        response = session.post(url, headers=headers, data=payload, verify=False)
        token = response.json()
        print(token)
        token = token["token"]
        if token is None:
            raise ValueError("No access token returned by the server.")
        return token
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def ping(authorization_token: str):
    response = requests.get(
        "https://apiext.tcbs.com.vn/asset-hub/v2/asset/overview?reload=true&accountNo=",
        headers={"Authorization": authorization_token},
        verify=False,
    )
    if response.status_code != 200:
        return False
    return True
