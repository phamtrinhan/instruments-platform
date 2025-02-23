from subprocess import PIPE, run
import platform
from grapebot import utils

def spcommand(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout.replace("\n", "")

if __name__ == "__main__":
    out = platform.machine()
    print(utils.today_in_ymd())