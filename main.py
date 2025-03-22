import datetime

import matplotlib.pyplot as plt
import akshare as ak
import numpy as np
import pandas as pd
from scipy.stats import percentileofscore

plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统可用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# symbol列表：https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/list
stock_dict = {
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

today = datetime.datetime.now().strftime("%Y%m%d")
# 创建一个空的 DataFrame 来存储结果
result_df = pd.DataFrame()

# 遍历 dict 的键
for symbol in stock_dict.keys():
    # 获取每个指数的历史数据
    df = ak.stock_zh_index_hist_csindex(symbol=symbol, start_date="20100101", end_date=today)

    # 提取并重命名市盈率列
    temp_df = df[['日期', '滚动市盈率', '收盘']].rename(
        columns={'滚动市盈率': stock_dict[symbol], '收盘': f"{stock_dict[symbol]}_收盘价"}).set_index('日期')

    # 按日期外连接合并
    if result_df.empty:
        result_df = temp_df
    else:
        result_df = result_df.join(temp_df, how='outer')

# 转换索引为datetime格式并排序
result_df.index = pd.to_datetime(result_df.index)
result_df.sort_index(inplace=True)

# 为每个标的计算滚动市盈率百分位
# 先获取原始列
original_columns = [col for col in result_df.columns if col in stock_dict.values()]

# 只遍历原始列
for col in original_columns:
    # 定义百分位计算函数（使用numpy数组提升性能）
    def calculate_pe_percentile(arr):
        current_value = arr[-1]
        if np.isnan(current_value):
            return np.nan
        historical_data = arr[~np.isnan(arr)]
        if len(historical_data) == 0:
            return np.nan
        return percentileofscore(historical_data, current_value, kind='rank')


    # 应用滚动计算（使用5年时间窗口）
    # 使用numpy数组格式提升性能
    # result_df[f'{col}_百分位'] = result_df[col].rolling('5Y', min_periods=1).apply(calculate_pe_percentile, raw=True)
    trading_days = 1260
    result_df[f'{col}_百分位'] = result_df[col].rolling(window=trading_days, min_periods=250).apply(
        calculate_pe_percentile, raw=True)

# 调整列顺序使相关数据相邻
new_columns_order = []
for col in original_columns:
    new_columns_order.extend([col, f'{col}_百分位', f'{col}_收盘价'])
result_df = result_df[new_columns_order]


# 绘制沪深300曲线
plt.figure(figsize=(16, 8))
ax1 = plt.gca()  # 第一个y轴（左）
ax2 = ax1.twinx()  # 第二个y轴（右，百分位）
ax3 = ax1.twinx()  # 第三个y轴（右，收盘价）

# 调整第三个轴的位置
ax3.spines['right'].set_position(('axes', 1.15))  # 向右偏移15%

# 绘制滚动市盈率
color_pe = 'tab:blue'
ax1.plot(result_df.index, result_df['沪深300'], color=color_pe, label='滚动市盈率')
ax1.set_ylabel('滚动市盈率', color=color_pe)
ax1.tick_params(axis='y', labelcolor=color_pe)

# 绘制百分位
color_percentile = 'tab:red'
ax2.plot(result_df.index, result_df['沪深300_百分位'], color=color_percentile,
        label='百分位', linestyle='--')
ax2.set_ylabel('百分位(%)', color=color_percentile)
ax2.tick_params(axis='y', labelcolor=color_percentile)
ax2.set_ylim(0, 100)

# 绘制收盘价
color_close = 'tab:green'
ax3.plot(result_df.index, result_df['沪深300_收盘价'], color=color_close,
       label='收盘价', linestyle='-.')
ax3.set_ylabel('收盘价', color=color_close)
ax3.tick_params(axis='y', labelcolor=color_close)


plt.title('沪深300滚动市盈率、历史百分位及收盘价（5年窗口）')
plt.tight_layout()

