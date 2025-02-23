from datetime import datetime
import os
from grapebot import storage
from grapebot.storage import local as local_storage
IGNORE_FOLDER = ['.DS_Store', 'cache', "__MACOSX__", "__MACOS__"]


def create_daily_file(path, date: datetime = datetime.today()):
    if path[0] != "/":
        path = "/" + path
    working_path = storage.DEFAULT_PATH_WITH_DATE + path
    file_path = working_path.format(home=os.getenv("HOME"),
                                    year=date.strftime("%Y"),
                                    month=date.strftime("%m"),
                                    day=date.strftime("%d"))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path


def create_global_file(path):

    if path[0] != '/':
        path = '/' + path
    working_path = storage.DEFAULT_PATH.format(home=os.getenv("HOME")) + path
    local_storage.create_folder_if_not_exist(working_path)
    return working_path


def get_data_path():
    return storage.DEFAULT_PATH.format(home=os.getenv("HOME"))


def check_file_exist(path):
    return os.path.exists(path)


def is_ignore(filename, folder=True):
    if filename in IGNORE_FOLDER:
        return False
    if folder:
        if "." in filename:
            return False

    return True


def remove_ignore_folder(folder_list):
    return list(filter(is_ignore, folder_list))
