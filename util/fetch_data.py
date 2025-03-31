import datetime

import akshare as ak
import pandas as pd

# 获取时需要关闭vpn
def fetch_index_data(stock_dict, start_date, end_date = datetime.datetime.now().strftime("%Y%m%d")):
    """获取并合并指数数据"""

    result_df = pd.DataFrame()

    for symbol, name in stock_dict.items():
        df = ak.stock_zh_index_hist_csindex(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )

        temp_df = df[['日期', '滚动市盈率', '收盘']].rename(
            columns={'滚动市盈率': name, '收盘': f"{name}_收盘价"}
        ).set_index('日期')

        result_df = result_df.join(temp_df, how='outer') if not result_df.empty else temp_df

    result_df.index = pd.to_datetime(result_df.index)
    return result_df.sort_index()
