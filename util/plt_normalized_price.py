import matplotlib.pyplot as plt
import pandas as pd
from util.fetch_data import fetch_index_data
from stock_enum.stock_enum import StockEnum
from stock_enum.data_index_enum import DataIndexEnum
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号

def plt_normalized_price(stocks=StockEnum):
    data_map = fetch_index_data(stocks)
    close_dfs = []
    for name, df in data_map.items():
        close = df[[DataIndexEnum.DATE.value, DataIndexEnum.CLOSE.value]].copy()
        # 归一化
        close[name] = close[DataIndexEnum.CLOSE.value] / close[DataIndexEnum.CLOSE.value].max()
        close = close[[DataIndexEnum.DATE.value, name]]
        close.set_index(DataIndexEnum.DATE.value, inplace=True)
        close_dfs.append(close)
    merged = pd.concat(close_dfs, axis=1)
    merged.plot(figsize=(12, 6))
    plt.title("归一化收盘价对比")
    plt.xlabel("日期")
    plt.ylabel("归一化收盘价")
    plt.legend()
    plt.savefig("normalized_price.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    stocks = [StockEnum.科创50, StockEnum.科创创业50]
    plt_normalized_price(stocks)
