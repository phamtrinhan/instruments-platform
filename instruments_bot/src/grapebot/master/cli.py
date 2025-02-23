import os
from grapebot.master import daily_master
from grapebot.master import total_merge
from grapebot.master.fireant import index_merger
from grapebot.master.fireant import fundamental

from grapebot.master.fireant import timescalemark
from grapebot.master.fireant import holders

from grapebot.master.ssi import map
from grapebot.master.notin import old_fundamental_utils
from grapebot.master.notin import fundamental_utils

from grapebot.master.fireant import liveshare as fant_liveshare
from grapebot.master.fireant import dividend as fant_dividends
from grapebot.master.notin import holc_merge as holc_tools

from grapebot.master.ssi import vn30f1m

from grapebot.master.tcbs import portfolio

from grapebot.tests import final_check


def main():
    print(
        "1. Execute daily\n2. Execute All History\n3. Excute from dates\n4. Get Fundamental ALL\n5. Get Organ mapping "
        "FIIN\n6. Get Timescale\n7. Build Fundamental\n8. Portfolio Download\n9. Automate check\n10.Fireant Holder fetch\n11. Liveshare Download\n12. VN30F1M\n13. Index Only\n14. Index Merger\n15. DIVIDENDS FIREANT\nYour select? ",
        end='')
    current_select = int(input())
    if current_select == 1:
        daily_master.main()
    elif current_select == 2:
        daily_master.main_hist()
    elif current_select == 3:
        print("Input start day dd/mm/yyyy: ", end="")
        start_day = input()
        # print(start_day.split())

        # dd, mm, yyyy = list(map(int, start_day.split('/')))
        daily_master.main_custom(start=start_day)
        total_merge.main_custom()
    elif current_select == 4:
        fundamental.main()
    elif current_select == 5:
        map.download()
    elif current_select == 6:
        timescalemark.get_custom()
    elif current_select == 7:
        fundamental_utils.main()

    elif current_select == 8:
        portfolio.download()

    elif current_select == 9:
        final_check.main()

    elif current_select == 10:
        holders.main()
    elif current_select == 11:
        fant_liveshare.download()

    elif current_select == 12:
        vn30f1m.main()

    elif current_select == 13:
        daily_master.daily_index_only()
    elif current_select == 14:
        index_merger.main()

    elif current_select == 15:
        fant_dividends.main_hist()
    elif current_select == 16:
        holc_tools.vn_index_and_all()
