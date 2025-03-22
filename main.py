import datetime
import matplotlib.pyplot as plt
import akshare as ak
import numpy as np
import pandas as pd
from scipy.stats import percentileofscore

# 全局配置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 指数配置
STOCK_DICT = {
    "000300": "沪深300",
    "000905": "中证500",
    "000852": "中证1000",
    "931573": "港股通科技",
    "399989": "医疗50",
    "000036": "消费30",
    "931412": "证券30",
    "931643": "科创创业50",
    "000688": "科创50",
}


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


def calculate_pe_percentiles(df, stock_dict, window=1260, min_periods=250):
    """计算市盈率百分位"""
    result_df = df.copy()
    original_columns = [name for name in stock_dict.values()]

    for col in original_columns:
        def _calculate(arr):
            current = arr[-1]
            if np.isnan(current): return np.nan
            hist = arr[~np.isnan(arr)]
            return percentileofscore(hist, current, 'rank') if len(hist) > 0 else np.nan

        result_df[f'{col}_百分位'] = result_df[col].rolling(
            window=window,
            min_periods=min_periods
        ).apply(_calculate, raw=True)

    return result_df


def reorder_columns(df, stock_dict):
    """调整列顺序"""
    new_order = []
    for name in stock_dict.values():
        new_order.extend([name, f'{name}_百分位', f'{name}_收盘价'])
    return df[new_order]


def plot_index_data(df, index_name):
    """绘制指数三轴图表"""
    fig, ax1 = plt.subplots(figsize=(16, 8))
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    # 设置第三个轴位置
    ax3.spines['right'].set_position(('axes', 1.15))

    # 绘制市盈率
    ax1.plot(df.index, df[index_name], 'b-', label='滚动市盈率')
    ax1.set_ylabel('市盈率', color='b')
    ax1.tick_params('y', colors='b')

    # 绘制百分位
    ax2.plot(df.index, df[f'{index_name}_百分位'], 'r--', label='历史百分位')
    ax2.set_ylabel('百分位(%)', color='r')
    ax2.tick_params('y', colors='r')
    ax2.set_ylim(0, 100)

    # 绘制收盘价
    ax3.plot(df.index, df[f'{index_name}_收盘价'], 'g-.', label='收盘价')
    ax3.set_ylabel('收盘价', color='g')
    ax3.tick_params('y', colors='g')

    # 合并图例
    lines = ax1.get_legend_handles_labels() + ax2.get_legend_handles_labels() + ax3.get_legend_handles_labels()
    fig.legend(
        [l for h in lines[::2] for l in h],
        [l for h in lines[1::2] for l in h],
        loc='upper left'
    )

    plt.title(f'{index_name}估值分析')
    plt.tight_layout()
    plt.show()


def main():
    # 数据获取
    raw_data = fetch_index_data(STOCK_DICT, start_date="20100101")

    # 特征计算
    processed_data = calculate_pe_percentiles(raw_data, STOCK_DICT)

    # 列排序
    final_df = reorder_columns(processed_data, STOCK_DICT)

    # 展示结果
    plot_index_data(final_df, '沪深300')


if __name__ == "__main__":
    main()
