import json
from datetime import datetime as dtime
import time
import pathlib
import random
import re
import pytz


from grapebot import log

HOSE_END_WORKING_HOURS = 17
logger = log.setup_logging('grapechain')


def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s


def random_number(length=5):
    return random.randint(length * 10, int('9' * length))


def get_current_folder():
    return pathlib.Path().resolve()


def print_key_dictionary(dictionary):
    for key, value in dictionary.items():
        print(key)


def check_request_is_okay(request_response_raw):
    if request_response_raw.status_code != 200:
        return False
    elif len(request_response_raw.text) > 0:
        return True
    else:
        return False


def get_response(request_response_raw):
    if check_request_is_okay(request_response_raw):
        return json.loads(request_response_raw.text)
    else:
        return {}


def object_to_json(data):
    json_string = json.dumps(data, indent=4)
    return json_string


''' 
    CREATE A DICTIONARY (TIME THREAD) TO STORE TIME START
'''
time_thread_dict = {}


def time_thread(thread_name='default'):
    global time_thread_dict
    if thread_name not in time_thread_dict:
        time_thread_dict[thread_name] = -1

    if time_thread_dict[thread_name] == -1:
        time_thread_dict[thread_name] = time.time()

        return "0 ms"
    else:
        temp_time_start = time_thread_dict[thread_name]
        time_thread_dict[thread_name] = -1

        return "{time:.2f} ms".format(
            time=(time.time() - temp_time_start) * 1000)


def c_load_json_file(file_path: str):
    from grapebot.storage import local as local_storage
    current_file_path = get_current_folder()
    file_path_real = "{}/{}".format(str(current_file_path), file_path)
    '''
        TODO: implement blocking outside project file path
        why:
            folder: project/grapechain/
            file_path: ../../a.json 
            load path will be ../project/a.json
            => this can became security vulnerable
    '''

    if not local_storage.check_file_exist(file_path_real):
        return None
    file_stream = open(file_path_real)
    data_in_file = json.load(file_stream)
    return data_in_file


def load_json_file(file_path: str):
    from grapebot.storage import local as local_storage
    if not local_storage.check_file_exist(file_path):
        return None
    '''
        TODO: implement blocking outside project file path
        why:
            folder: project/grapechain/
            file_path: ../../a.json
            load path will be ../project/a.json
            => this can became security vulnerable
    '''
    with open(file_path, "r") as file:
        data_in_file = json.load(file)
        return data_in_file


def write_json_file(file_path, data):
    from .storage.local import create_folder_if_not_exist
    '''
        TODO: implement blocking outside project file path
        why:
            folder: project/grapechain/
            file_path: ../../a.json 
            load path will be ../project/a.json
            => this can became security vulnerable
    '''
    create_folder_if_not_exist(file_path)

    with open(file_path, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    outfile.close()
    return True


def set_key_json_file(key, value, json_file):
    data = load_json_file(json_file)
    data[key] = value
    write_json_file(json_file, data)
    return True


def get_key_json_file(key, json_file):
    data = load_json_file(json_file)
    if key not in data:
        data[key] = ""
    return data[key]


def year():
    return dtime.today().strftime("%Y")


def month():
    return dtime.today().strftime("%m")


def quarter():
    current_month = int(month())
    return str(current_month // 3 + 1)


def today_in_ymd(dash=False):
    if dash:
        return dtime.today().strftime("%Y_%m_%d")
    return dtime.today().strftime('%Y-%m-%d')


def today_in_vnd_dmy():
    return dtime.today().strftime('%d/%m/%Y')


def today_not_in():
    return dtime.today().strftime('%d%m%Y')


def today_in_unix():
    return int(time.time())


def unix_to_ymd(date=today_in_unix()):
    return dtime.fromtimestamp(date)


def ymd_to_unix(date=today_in_ymd()):
    return int(dtime.strptime(date, "%Y-%m-%d").timestamp())


def today_in_vn_format():
    return dtime.today().strftime("%d.%m.%Y")


def end_working_date_in_vn_format():
    today = dtime.today()
    if today.hour > HOSE_END_WORKING_HOURS:
        today
    today -= dtime.timedelta(days=1)
    return today.strftime("%d.%m.%Y")


def dmy_to_ymd(input):
    start = input.split('/')
    if len(start[-1]) == 4:
        start_n = f"{start[-1]}-{start[-2]}-{start[-3]}"
    else:
        start_n = input
    return start_n


def ymd_to_dmy(input):
    start = input.split('-')
    if len(start[0]) == 4:
        start_n = f"{start[-1]}/{start[-2]}/{start[-3]}"

    else:
        start_n = input
    return start_n


def ymd_to_dmy(input):
    start = input.split('-')
    if len(start[0]) == 4:
        start_n = f"{start[-1]}/{start[-2]}/{start[-3]}"

    else:
        start_n = input
    return start_n


def select_attr_from_dict(input_dict, attr):
    # print(input_dict)
    for key, value in input_dict.items():
        for items_attr, value_stock in list(input_dict[key].items()):
            if items_attr not in attr:
                del input_dict[key][items_attr]
    return input_dict


def today_morning_in_unix():
    morning = dtime.now(pytz.timezone('GMT')).replace(
        hour=0, minute=0, second=0, microsecond=0)
    return int(morning.timestamp())


def today_end_in_unix():
    evening = dtime.now(pytz.timezone('GMT')).replace(
        hour=21, minute=0, second=0, microsecond=0)
    return int(evening.timestamp())


def smap(f):
    return f()


def merge_dict(dict_one, dict_two):
    return {*dict_one, *dict_two}
