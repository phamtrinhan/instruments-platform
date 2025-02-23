import json
import os
from glob import glob
from grapebot.storage import local as storage_local
import logging
logger = logging.getLogger()

CREDENTIAL_PATH = "%s/grapechain/credentials/ssi_fcdata.json" % (
    os.getenv("HOME"))
AUTH_PATH = "https://fc-data.ssi.com.vn/api/v2/Market/AccessToken"


def load_credentials():
    return json.load(open(CREDENTIAL_PATH))


def consumerId():
    return load_credentials()["consumerID"]


def consumerSecret():
    return load_credentials()["consumerSecret"]


def get_token():
    credential = load_credentials()
    logger.info(credential)
    token = authorize()
    credential["token"] = token
    with open(CREDENTIAL_PATH, 'w') as f:
        json.dump(credential, f)
    token: str = credential["token"]
    return token


def authorize():
    import requests
    response = requests.post(AUTH_PATH, json={

        "consumerID": consumerId(),
        "consumerSecret": consumerSecret()
    })
    logger.info(response.json())
    return response.json()['data']["accessToken"]
