import matplotlib.pyplot as plt


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
