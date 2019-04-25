from Models.SubscribeModels.Base.BaseSubscribeModel import BaseSubscribeModel


class Price(BaseSubscribeModel):
    ask = 0.0
    ask_volume = 0
    bid = 0.0
    bid_volume = 0
    close = 81.0
    high = 0.0
    last = 0.0
    last_volume = 0
    low = 0.0
    open = 0.0
    tick_timestamp = 0
    trade_timestamp = 0
    turnover = 0.0
    turnover_volume = 0
    vwap = 0.0

    def __init__(self, i, m):
        super().__init__(i, m)
