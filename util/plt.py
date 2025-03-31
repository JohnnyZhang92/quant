import matplotlib.pyplot as plt


def plot_index_data(df, index_name, low_percentile=30, high_percentile=60):
    """绘制指数三轴图表（百分位分段着色）"""
    fig, ax1 = plt.subplots(figsize=(16, 8))
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    # 设置第三个轴位置
    ax3.spines['right'].set_position(('axes', 1.15))

    # 绘制市盈率（保持原蓝色）
    ax1.plot(df.index, df[index_name], 'y-', label='滚动市盈率')
    ax1.set_ylabel('市盈率', color='y')
    ax1.tick_params('y', colors='y')

    # 准备百分位数据
    percentile = df[f'{index_name}_百分位']

    # 创建分段掩码
    mask_low = percentile <= low_percentile
    mask_mid = (percentile > low_percentile) & (percentile < high_percentile)
    mask_high = percentile >= high_percentile

    # 分段绘制百分位线
    ax2.plot(df.index[mask_low], percentile[mask_low], 'b', linestyle='--', label='低估值区间')
    ax2.plot(df.index[mask_mid], percentile[mask_mid], 'gray', linestyle='--', label='中估值区间')
    ax2.plot(df.index[mask_high], percentile[mask_high], 'r', linestyle='--', label='高估值区间')

    ax2.set_ylabel('百分位(%)', color='k')
    ax2.tick_params('y')
    ax2.set_ylim(0, 100)

    # 绘制收盘价（保持原绿色）
    ax3.plot(df.index, df[f'{index_name}_收盘价'], 'g-.', label='收盘价')
    ax3.set_ylabel('收盘价', color='g')
    ax3.tick_params('y', colors='g')

    # 合并图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    # 自定义图例条目顺序
    all_handles = handles1 + [handles2[0], handles2[2]] + handles3
    all_labels = labels1 + [labels2[0], labels2[2]] + labels3

    fig.legend(all_handles, all_labels, loc='upper left', bbox_to_anchor=(0.12, 0.88))

    plt.title(f'{index_name}估值分析（蓝:≤{low_percentile}% 红:≥{high_percentile}%）')
    plt.tight_layout()
    plt.show()
