import numpy as np
from scipy.stats import percentileofscore


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
