from typing import TypedDict
import pandas as pd
from .._model import Model


class RelativeStrengthModel(Model):
    @staticmethod
    def _get_changes(prices):
        changes = prices.diff(periods=1)
        return changes


class SRS_CFG(TypedDict):
    window: int


class SimpleRelativeStrengthModel(RelativeStrengthModel):
    def __init__(self, prices, CFG: SRS_CFG):
        self.prices = prices.rename("price")
        self.CFG = CFG

    def indicator(self):
        changes = self._get_changes(self.prices)

        gains = changes.where(changes > 0, 0).rolling(window=self.CFG["window"]).mean()
        losses = changes.where(changes < 0, 0).rolling(window=self.CFG["window"]).mean()

        rs = gains / abs(losses)
        rsi = (100 - (100 / (1 + rs))).rename("rsi")

        indicator = pd.concat([self.prices, rsi], axis=1)
        return indicator

    def signal(self, indicator: pd.DataFrame, continious: bool, trend: bool):
        if continious:
            signal = self._continuous_signal(indicator)
        else:
            signal = self._discreate_signal(indicator)
        if trend:
            signal["signal"] = signal["signal"] * -1
        return signal

    def _discreate_signal(self, indicator):
        signal=indicator.copy()
        signal["signal"] = 0.0

        over_buy = 70 <= signal["rsi"]
        signal.loc[over_buy, "signal"] = -1

        over_sell = signal["rsi"] <= 30
        signal.loc[over_sell, "signal"] = 1
        return signal

    def _continuous_signal(self, indicator):
        signal = self._discreate_signal(indicator)

        def _rsi_signal(rsi):
            return (50 - rsi) / 50

        signal.loc[:, "signal"] = signal["rsi"].apply(lambda x: _rsi_signal(x))
        return signal
