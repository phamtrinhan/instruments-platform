from grapebot.master.fireant import holc as fant_holc
from grapebot.master.fireant import index_merger

from grapebot.master.notin import holc_merge as holc_tools

from grapebot import log
from grapebot import telegram
from grapebot.master.entradex import porfolio
from grapebot import utils
logger = log.get_logger('daily_master.log')


def main_custom():
    # holc.main()
    telegram.send_message("Start gen all YAML and Merge base to total")
    holc_tools.fant_merge_custom()
    holc_tools.ssi_merge_custom()
    holc_tools.liveshare_merge_custom()
    holc_tools.gen_sector()
    holc_tools.vn_index_and_all()
    telegram.send_message("Merge done!")

# @process.tracker(logger=logger)


def main_hist():
    # holc.main()
    telegram.send_message("Start gen all YAML and Merge base to total ALL")
    holc_tools.fant_merge_base()
    # holc_tools.ssi_merge_base()
    holc_tools.liveshare_merge()
    index_merger.main()

    holc_tools.gen_sector()
    holc_tools.fireant_dividend_merge()
    holc_tools.vn_index_and_all()

    telegram.send_message("Merge done!")


def main():
    telegram.send_message("Start gen YAML Daily")
    holc_tools.fant_merge_base_daily()
    holc_tools.liveshare_merge()
    holc_tools.gen_sector()
    holc_tools.vn_index_and_all()

    telegram.send_message("Merge done!")


if __name__ == "__main__":
    # fireant_daily.download_instruments()
    main()
