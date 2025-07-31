from enum import Enum


class DataIndexEnum(Enum):
    DATE = "日期"
    INDEX_CODE = "指数代码"
    INDEX_CHINESE_SHORT_NAME = "指数中文简称"
    INDEX_ENGLISH_SHORT_NAME = "指数英文简称"
    OPEN = "开盘"
    HIGH = "最高"
    LOW = "最低"
    CLOSE = "收盘"
    CHANGE = "涨跌"
    CHANGE_PERCENT = "涨跌幅"
    VOLUME = "成交量"
    AMOUNT = "成交金额"
    SAMPLE_COUNT = "样本数量"
    ROLLING_PE = "滚动市盈率"
