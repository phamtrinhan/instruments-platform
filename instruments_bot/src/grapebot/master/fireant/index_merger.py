
import pandas as pd
from grapebot.storage import utils as storage_utils


def main():

    today_path = storage_utils.create_daily_file(
        "notion/HIST_FIREANT_HOLC/INDEX/")
    df = pd.read_csv(today_path + "base.csv")
    vn30d = df[df['symbol'] == "VN30"].to_dict('records')
    df_d = []
    for vn30 in vn30d:
        df_d.append(
            {
                "date": pd.to_datetime(vn30['date']),
                "Open": vn30['priceOpen'],
                "High": vn30['priceHigh'],
                "Price": vn30['priceClose'],
                "Low": vn30['priceLow'],
                "Volume": vn30['totalVolume']
            })
    df_new = pd.DataFrame(df_d)
    df_new.index = df_new['date']
    df_new = df_new.drop(columns=["date"])
    storage_vn30 = storage_utils.create_global_file("total/vn30_index.csv")
    vn30_trade_op = pd.read_csv(storage_vn30, index_col=0, parse_dates=True)
    vn30_data_merge = pd.concat([vn30_trade_op, df_new])
    vn30_data_merge = vn30_data_merge[~vn30_data_merge.index.duplicated(
        keep='first')].sort_index()
    vn30_data_merge = vn30_data_merge.drop_duplicates()
    vn30_data_merge.to_csv(storage_vn30)
    df = pd.read_csv(today_path + "base.csv")

    vnindex_d = df[df['symbol'] == "VNINDEX"].to_dict('records')
    vni_f = []
    for vnindex in vnindex_d:
        vni_f.append({
            "date": pd.to_datetime(vnindex['date']),
            "Open": vnindex['priceOpen'],
            "High": vnindex['priceHigh'],
            "Price": vnindex['priceClose'],
            "Low": vnindex['priceLow'],
            "Volume": vnindex['totalVolume']
        })

    df_vni_new = pd.DataFrame(vni_f)
    print(df_vni_new)

    df_vni_new.index = df_vni_new['date']
    df_vni_new = df_vni_new.drop(columns=["date"])
    storage_vni = storage_utils.create_global_file("total/vn_index.csv")

    vni_trade_op = pd.read_csv(storage_vni, index_col=0, parse_dates=True)

    vni_dm = pd.concat([vni_trade_op, df_vni_new])
    vni_dm = vni_dm[~vni_dm.index.duplicated(keep='first')].sort_index()
    vni_dm = vni_dm.drop_duplicates()
    vni_dm.to_csv(storage_vni)
