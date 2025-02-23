from datetime import datetime
import os
import time
cwd = os.getcwd()

with open(os.path.join(cwd, "log_cron.txt"), "a") as f:
    f.write("Accessed cron.py on " + str(datetime.now()) + "\n")
print("Accessed cron.py on " + str(datetime.now()) + "\n")
import requests
time.sleep(3)
url = "https://svr8.fireant.vn/api/Data/Markets/IntradayQuotes?symbol=VN30F1M"

payload = {}
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxOTc4Nzk5OTQ4LCJuYmYiOjE2Nzg3OTk5NDgsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsInJvbGVzIiwiZW1haWwiLCJhY2NvdW50cy1yZWFkIiwiYWNjb3VudHMtd3JpdGUiLCJvcmRlcnMtcmVhZCIsIm9yZGVycy13cml0ZSIsImNvbXBhbmllcy1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImZpbmFuY2UtcmVhZCIsInBvc3RzLXdyaXRlIiwicG9zdHMtcmVhZCIsInN5bWJvbHMtcmVhZCIsInVzZXItZGF0YS1yZWFkIiwidXNlci1kYXRhLXdyaXRlIiwidXNlcnMtcmVhZCIsInNlYXJjaCIsImFjYWRlbXktcmVhZCIsImFjYWRlbXktd3JpdGUiLCJibG9nLXJlYWQiLCJpbnZlc3RvcGVkaWEtcmVhZCJdLCJzdWIiOiJlYTY3MTQ2ZS00MzJhLTQ5ZjgtODAzMi1kNzg1Nzk5ZGRlYzUiLCJhdXRoX3RpbWUiOjE2Nzg3OTk5NDgsImlkcCI6Imlkc3J2IiwibmFtZSI6Im9saXZpZXIubmd1eWVuLmZyQGdtYWlsLmNvbSIsInNlY3VyaXR5X3N0YW1wIjoiNzU2ZTRlMjAtODUwZi00Mjg3LWJjYjUtNzVkOWNhZjk5ZGU0IiwianRpIjoiNzQyMGJlOGY5MmJlYWNkMWFjMjIwZDQwMDNlZGJmYjIiLCJhbXIiOlsicGFzc3dvcmQiXX0.CNtRe9QTG8FhNIFCKLMSHcG2z_7VfATH8aXW06vUUGU_cYCxjyxdS_j7VAnOLVqlMAT_HozgAMJVw37WDebRrZUBhzocmdDqOgh9bHYKgngRBCvClx_cpPhPSIGpgFyOdPZz21xTqu3yV39AI50Am59VnwSAiC9x5pMgxmLd_Q4F7XFr335tf_h2EGAEyy2vPh4OTjgEhZiUuRsospt_rkZpbI1Iuyh7hsQfJJA14ea8f2-_tXojhUup7gqhL8UiM9o48TMXTo45Nj5x-8g8L__ts2UH19Po0bgDJsP71SrOYSoH2k48x7yMUBMYlJG3ybFvJ9ULJvwLg3LIj5NbJA',
    'Cookie': 'ASP.NET_SessionId=fhf4buuayuktvdqrpnnwqoww'
}

response = requests.request("GET", url, headers=headers, data=payload)


def check_file_exist(file_path):
    return Path(file_path).is_file()


import json
# from datetime import datetime as datetime
import time
import pathlib
import random
import re

HOSE_END_WORKING_HOURS = 17


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


def get_credentials():
    if not check_file_exist(
            f"{DEFAULT_PATH}/credentials/telegram.json"):
        write_json_file(f"{DEFAULT_PATH}/credentials/telegram.json", {})

    credentials = load_json_file(
        f"{DEFAULT_PATH}/credentials/telegram.json")
    if ('token' not in credentials.keys()) or (not credentials['token']):
        raise Exception("Token Telegram not found")
    else:
        return credentials


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

    if not check_file_exist(file_path_real):
        return None
    file_stream = open(file_path_real)
    data_in_file = json.load(file_stream)
    return data_in_file


def load_json_file(file_path: str):
    if not check_file_exist(file_path):
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


def save_object_to_file(data, source, file_name='today_in_ymd', path=''):
    if source != "":

        json_string = object_to_json(data)
        # today_ymd = utils.today_in_ymd()

        storing_path = "{}/grapechain/data/".format(os.getenv("HOME")).format(**locals(), **globals()) if (
                path == '') else path.format(**locals(), **globals())
        create_folder_if_not_exist(storing_path)
        #
        with open(storing_path, 'w') as output_stream:
            output_stream.write(json_string)
        return storing_path
    else:
        raise Exception('Error')


def write_json_file(file_path, data):
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
    return datetime.today().strftime("%Y")


def month():
    return datetime.today().strftime("%m")


def quarter():
    current_month = int(month())
    return str(current_month // 3 + 1)


def today_in_ymd(dash=False):
    if dash:
        return datetime.today().strftime("%Y_%m_%d")
    return datetime.today().strftime('%Y-%m-%d')


def today_in_vnd_dmy():
    return datetime.today().strftime('%d/%m/%Y')


def today_not_in():
    return datetime.today().strftime('%d%m%Y')


def today_in_unix():
    return int(time.time())


def unix_to_ymd(date=today_in_unix()):
    return datetime.fromtimestamp(date)


def ymd_to_unix(date=today_in_ymd()):
    return int(datetime.strptime(date, "%Y-%m-%d").timestamp())


def today_in_vn_format():
    return datetime.today().strftime("%d.%m.%Y")


def end_working_date_in_vn_format():
    today = datetime.today()
    if today.hour > HOSE_END_WORKING_HOURS:
        today
    today -= datetime.timedelta(days=1)
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


def smap(f):
    return f()


def merge_dict(dict_one, dict_two):
    return {*dict_one, *dict_two}


from datetime import date
import os
from pathlib import Path

today = date.today()
today_in_ymd = today_in_ymd()

import requests
import logging
import os

logger = logging.getLogger()
TELEGRAM_SEND_MESSAGE = "https://api.telegram.org/bot{token}/sendMessage"
DEFAULT_PATH = "{HOME}/grapechain".format(HOME=os.getenv("HOME"))


def get_token(credentials=get_credentials()):
    return credentials['token']


def get_main_group(credentials=get_credentials()):
    return credentials['main_group_id']


def get_group_id_default(credentials=get_credentials()):
    return credentials['group_id']


def o_send_message(message, chat_id=get_group_id_default(), token=get_token()):
    payloads = {
        'text': message,
        'chat_id': chat_id
    }
    response = requests.post(TELEGRAM_SEND_MESSAGE.format(token=token),
                             json=payloads)
    return get_response(response)['ok']


def send_message(message, chat_id=get_group_id_default(), token=get_token()):
    if os.getenv("TELEGRAM_DEV") == "1" or os.getenv("TELEGRAM_DEV") == 1:
        return

    payloads = {
        'text': message,
        'chat_id': chat_id
    }
    response = requests.post(TELEGRAM_SEND_MESSAGE.format(token=token),
                             json=payloads)
    # print(response.text)
    if 'ok' in get_response(response):
        return get_response(response)['ok']
    else:
        return False


def create_folder_if_not_exist(path):
    temp_path = path.split('/')
    if temp_path[-1].find('.') > -1:
        path = '/'.join(temp_path[:-1])
    if not os.path.exists(path):
        os.makedirs(path)


def write(path, data):
    json_string = object_to_json(data)
    # today_ymd = utils.today_in_ymd()

    storing_path = path
    create_folder_if_not_exist(storing_path)
    #
    with open(storing_path, 'w') as output_stream:
        output_stream.write(json_string)
    output_stream.close()


import json

from datetime import datetime, timedelta

write("{HOME}/grapechain/cron/output/".format(HOME=os.getenv("HOME")) + datetime.now().strftime(
    "%d-%b-%Y-%H:%M:%S") + '.json', json.loads(response.text))
data = json.loads(response.text)

last_minute = datetime.utcnow() - timedelta(minutes=2)
last_minute_2 = datetime.utcnow() - timedelta(minutes=3)

# Filter data for the last minute only
filtered_data = [item for item in data if datetime.strptime(item['Date'], "%Y-%m-%dT%H:%M:%SZ") >= last_minute]
filtered_data_2 = [item for item in data if datetime.strptime(item['Date'], "%Y-%m-%dT%H:%M:%SZ") < last_minute and datetime.strptime(item['Date'], "%Y-%m-%dT%H:%M:%SZ") > last_minute_2]

high = filtered_data[0]['Price']
low = filtered_data[0]['Price']
open_price = filtered_data[0]['Price']
close_price = filtered_data[-1]['Price']
total_volume = 0
for item in filtered_data:
    price = item['Price']
    volume = item['Volume']

    if price > high:
        high = price

    if price < low:
        low = price

    total_volume += volume

high_2 = filtered_data_2[0]['Price']
low_2 = filtered_data_2[0]['Price']
open_price_2 = filtered_data_2[0]['Price']
close_price_2 = filtered_data_2[-1]['Price']
total_volume_2 = 0

for item in filtered_data_2:
    price_2 = item['Price']
    volume_2 = item['Volume']

    if price_2 > high_2:
        high_2 = price_2

    if price_2 < low_2:
        low_2 = price_2

    total_volume_2 += volume_2
change = {'close': close_price_2 - close_price, 'high': high_2 - high, 'low': low_2 - low, 'open_price': open_price_2 - open_price, 'total_volume': total_volume_2 - total_volume}
change_percentage = {
    'close': (close_price_2 - close_price) / close_price * 100 if close_price != 0 else 0.0,
    'total_volume': (total_volume_2 - total_volume) / total_volume * 100 if total_volume != 0 else 0.0
}
import pytz
utc_plus_7 = pytz.timezone('Asia/Bangkok')

df = filtered_data[-1]
df['Date'] = datetime.strptime(df['Date'], "%Y-%m-%dT%H:%M:%SZ")
utc_time = pytz.utc.localize(df['Date'])
local_time = utc_time.astimezone(utc_plus_7)
df['Date'] = local_time

message = f'== Ngày: {df["Date"].strftime("%Y-%m-%d lúc %H:%M")} ==\n' \
          f"Giá đóng: {close_price_2} ({change['close']:.2f} điểm | {change_percentage['close']:.2f}%)\n" \
          f"Số lượng hợp đồng: {total_volume_2} (thay đổi {change['total_volume']:.2f} | {change_percentage['total_volume']:.2f}%)\n" \
          f"Tổng trong ngày: {df['TotalVolume']}\n" \
          f'ID: {df["ID"]}-{df["Symbol"]} \n==='

# print(message)
send_message(message, '-1001873871501')