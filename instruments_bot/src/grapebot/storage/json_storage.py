
from .. import *
from ..set_time import *
from .. import utils
from .. import log

from datetime import date
import os
from pathlib import Path


logger = log.setup_logging('grapechain')

today = date.today()
today_in_ymd = utils.today_in_ymd()


def create_folder_if_not_exist(path):
    temp_path = path.split('/')
    if temp_path[-1].find('.') > -1:
        path = '/'.join(temp_path[:-1])
    if not os.path.exists(path):
        os.makedirs(path)


def write(path, data):

    json_string = utils.object_to_json(data)
    # today_ymd = utils.today_in_ymd()

    storing_path = path
    create_folder_if_not_exist(storing_path)
    #
    with open(storing_path, 'w') as output_stream:
        output_stream.write(json_string)
    output_stream.close()


def check_file_exist(file_path):
    return Path(file_path).is_file()
