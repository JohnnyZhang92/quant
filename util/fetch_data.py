import datetime
import akshare as ak
from stock_enum.stock_enum import StockEnum


# 获取时需要关闭vpn
def fetch_index_data(stocks=StockEnum, start_date="20150101", end_date=datetime.datetime.now().strftime("%Y%m%d")):
    result = {}
    for stock in stocks:
        df = ak.stock_zh_index_hist_csindex(
            symbol=stock.value,
            start_date=start_date,
            end_date=end_date
        )

        result[stock.name] = df

    return result
