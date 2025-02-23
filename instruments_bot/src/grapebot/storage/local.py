
from grapebot import utils

from datetime import date
import os
from pathlib import Path


today = date.today()
today_in_ymd = utils.today_in_ymd()


def create_folder_if_not_exist(path):
    temp_path = path.split('/')
    if temp_path[-1].find('.') > -1:
        path = '/'.join(temp_path[:-1])
    if not os.path.exists(path):
        os.makedirs(path)


def save_object_to_file(data, source, file_name=today_in_ymd, path=''):
    if source != "":

        json_string = utils.object_to_json(data)
        # today_ymd = utils.today_in_ymd()

        storing_path = "{}/grapechain/data/".format(os.getenv("HOME")).format(**locals(), **globals()) if (path == '') else path.format(**locals(), **globals())
        create_folder_if_not_exist(storing_path)
        #
        with open(storing_path, 'w') as output_stream:
            output_stream.write(json_string)
        return storing_path
    else:
        raise Exception('Error')


def check_file_exist(file_path):
    return Path(file_path).is_file()
