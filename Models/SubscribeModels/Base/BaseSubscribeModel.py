class BaseSubscribeModel:
    i = ""  # The tradable identifier or indicator identifier. Used for "price", "depth", "trade", "indicator" and
    # "trading_status".

    m = 0  # The tradable market_id or indicator src. If . Used for "price", "depth", "trade", "indicator" and
    # "trading_status". If this is used for "indicator" the field is a string otherwise an integer.

    def __init__(self, i, m):
        self.i = i
        self.m = m
