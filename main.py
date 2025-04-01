import matplotlib.pyplot as plt

from util.fetch_data import fetch_index_data
from util.pe import *
from util.plt import plot_index_data

# 全局配置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 指数配置
# 映射关系搜https://www.csindex.com.cn/zh-CN/indices/index-detail/H30374#/indices/family/list
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
    "000922": "中证红利",
}


def main():
    # 数据获取
    raw_data = fetch_index_data(STOCK_DICT, start_date="20100101")

    # 特征计算
    processed_data = calculate_pe_percentiles(raw_data, STOCK_DICT)

    # 列排序
    final_df = reorder_columns(processed_data, STOCK_DICT)

    # 展示结果
    plot_index_data(final_df, '中证红利')


if __name__ == "__main__":
    main()
