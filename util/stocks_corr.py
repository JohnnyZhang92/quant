import pandas as pd
from util.fetch_data import fetch_index_data
from stock_enum.stock_enum import StockEnum
from stock_enum.data_index_enum import DataIndexEnum


def stocks_corr(stocks=StockEnum):
    data_map = fetch_index_data(stocks)
    close_dfs = []
    for name, df in data_map.items():
        # 只保留日期和收盘价，并重命名收盘价列为股票名
        close_df = df[[DataIndexEnum.DATE.value, DataIndexEnum.CLOSE.value]].copy()
        close_df = close_df.rename(columns={DataIndexEnum.CLOSE.value: name})
        close_df.set_index(DataIndexEnum.DATE.value, inplace=True)
        close_dfs.append(close_df)

    # 按日期对齐合并
    merged_close = pd.concat(close_dfs, axis=1)

    # 排除有缺失的行
    # merged_close = merged_close.dropna()

    # 计算相关性
    corr_matrix = merged_close.corr().round(2)
    corr_matrix['mean'] = corr_matrix.mean().round(2)
    sort_matrix = corr_matrix.sort_values(by='mean', ascending=False)
    for name in sort_matrix.index:
        if name == 'mean':
            continue
        value = StockEnum[name].value
        print(f"StockEnum.{name},")
    print(corr_matrix)


if __name__ == "__main__":
    stocks = [
        StockEnum.科创50,
        # StockEnum.化工,
        # StockEnum.全指信息,
        StockEnum.医疗50,
        # StockEnum.半导体,
        StockEnum.恒生科技,
        StockEnum.证券30,
        StockEnum.中证2000,
        StockEnum.煤炭,
    ]
    stocks_corr(stocks)
