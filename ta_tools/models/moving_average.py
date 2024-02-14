from typing import TypedDict
import pandas as pd
from .._model import Model


class MovingAverageModel(Model):
    @staticmethod
    def _get_ma_series(series, window):
        ma_series = series.rolling(window=window).mean()
        return ma_series


class DMA_CFG(TypedDict):
    short_window: int
    long_window: int


class SimpleMovingAverageModel(MovingAverageModel):
    def __init__(self, prices: pd.Series, CFG: DMA_CFG):
        self.prices = prices.rename("price")
        self.CFG = CFG

    def indicator(self):
        short_ma_series = self._get_ma_series(self.prices, self.CFG["short_window"])
        short_ma_series.rename("short_ma", inplace=True)
        
        long_ma_series = self._get_ma_series(self.prices, self.CFG["long_window"])
        long_ma_series.rename("long_ma", inplace=True)
        
        indicator = pd.concat([self.prices, short_ma_series, long_ma_series], axis=1)
        return indicator

    def signal(self, indicator: pd.DataFrame, continious: bool, trend: bool):
        if continious:
            signal = self._continuous_signal(indicator)
        else:
            signal = self._discreate_signal(indicator)
        if not trend:
            signal["signal"] = signal["signal"] * -1
        return signal

    def _continuous_signal(self, indicator):
        signal = self._discreate_signal(indicator)
        ma_diff = signal["short_ma"] - signal["long_ma"]
        normalized_ma_diff = ma_diff / ma_diff.abs().rolling(window=100).max()
        signal.loc[:, "signal"] = normalized_ma_diff
        return signal

    def _discreate_signal(self, indicator):
        signal = indicator.copy()
        signal["signal"] = 0

        gold_cross_condition = (signal["short_ma"].shift(1) < signal["long_ma"]) & (
            signal["short_ma"] > signal["long_ma"]
        )
        signal.loc[gold_cross_condition, "signal"] = 1

        dead_cross_condition = (signal["short_ma"].shift(1) > signal["long_ma"]) & (
            signal["short_ma"] < signal["long_ma"]
        )
        signal.loc[dead_cross_condition, "signal"] = -1
        return signal
