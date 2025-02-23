import os
import pandas as pd
from grapebot import process
from grapebot import log
from grapebot import telegram
from grapebot import utils
from grapebot.master.fireant import fundamental
from grapebot.master.entradex import vn30f1m
from grapebot.master.tcbs.assets import main as tcbs_assets
from grapebot.master.tcbs.portfolio import main as tcbs_portfolio
from grapebot.master.fireant import dividend as fant_dividends

from grapebot.storage import utils as storage_utils

logger = log.get_logger("daily_master.log")


@process.main_tracker(logger=logger)
def main():
    # holc.main()
    from grapebot.master.fireant import holc as fant_holc
    from grapebot.master.fireant import liveshare as fant_liveshare

    telegram.send_message("---- DEBUG MODE: ON ----")
    telegram.send_message("---- Start crawling ----")
    telegram.send_message(f"Start at {utils.today_in_vn_format()}")
    # telegram.send_message("Start SSI: HOLC")
    # ssi_holc.main()

    # telegram.send_message("✅ SSI Complete !")
    telegram.send_message("Start FIREANT: HOLC")
    fant_holc.main()
    #

    telegram.send_message("✅ FANT Complete ! ")
    telegram.send_message("Start FIREANT: Liveshare")

    fant_liveshare.download()
    telegram.send_message("Start SSI+FIREANT: Fundamental")

    fundamental.main()

    # telegram.send_message("Building Sector")

    # ssi_sector.main()

    telegram.send_message("✅ DONE")

    telegram.send_message("---- DONE ----")


def main_hist():
    # holc.main()
    from grapebot.master.fireant import holc as fant_holc
    from grapebot.master.fireant import liveshare as fant_liveshare

    telegram.send_message("---- DEBUG MODE: ON ----")
    telegram.send_message("---- Start crawling ----")
    telegram.send_message(f"Start at {utils.today_in_vn_format()}")
    # telegram.send_message("Start SSI: HOLC")
    # ssi_holc.main_hist()

    # telegram.send_message("✅ SSI Complete !")
    telegram.send_message("Start FIREANT: HOLC")
    fant_holc.main_hist()

    fant_holc.index_only()
    #
    vn30f1m.main()

    telegram.send_message("✅ FANT Complete ! ")

    telegram.send_message("Start FIREANT: Liveshare")

    fant_liveshare.download()
    telegram.send_message("Start FIREANT: Dividend")
    fant_dividends.main_hist()

    telegram.send_message("Start TCBs: Assets")
    tcbs_assets()
    telegram.send_message("Start TCBs: Portfolio")
    tcbs_portfolio()

    telegram.send_message("Building Sector")
    fundamental.main()

    # ssi_sector.main()

    telegram.send_message("✅ DONE")


def daily_index_only():
    from grapebot.master.fireant import holc as fant_holc

    fant_holc.index_only()


def main_custom(start=None, end=None):
    # holc.main()
    from grapebot.master.fireant import holc as fant_holc
    from grapebot.master.fireant import liveshare as fant_liveshare
    from grapebot.master.ssi import holc as ssi_holc
    from grapebot.master.ssi import sector as ssi_sector

    telegram.send_message("---- DEBUG MODE: ON ----")
    telegram.send_message("---- Start crawling ----")
    telegram.send_message(f"Start at {utils.today_in_vn_format()}")
    telegram.send_message("Start SSI: HOLC")
    # ssi_holc.main_custom(start=start, end=None)

    telegram.send_message("✅ SSI Complete !")
    telegram.send_message("Start FIREANT: HOLC")
    fant_holc.get_custom(start=start, end=None)
    #

    telegram.send_message("✅ FANT Complete ! ")

    telegram.send_message("Start FIREANT: Liveshare")

    fant_liveshare.download()
    telegram.send_message("Building Sector")

    # ssi_sector.main()

    telegram.send_message("✅ DONE")


if __name__ == "__main__":
    # fireant_daily.download_instruments()
    main()
