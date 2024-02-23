from typing import TypedDict
import pandas as pd
from .._model import Model


class SBB_CFG(TypedDict):
    window: int
    n: int


class BollingerBandModel(Model):
    @staticmethod
    def _get_rolled_series(series, window):
        rolled_series = series.rolling(window=window)
        return rolled_series

    @staticmethod
    def _get_band_width(rolled_series, n):
        band_width = rolled_series.std() * n
        return band_width


class SimpleBollingerBandModel(BollingerBandModel):
    def __init__(self, prices: pd.Series, CFG: SBB_CFG) -> None:
        self.prices = prices.rename("price")
        self.CFG = CFG

    def indicator(self) -> pd.DataFrame:
        rolled_prices = self._get_rolled_series(self.prices, self.CFG["window"])
        ma_price = rolled_prices.mean().rename("ma_price")

        band_width = self._get_band_width(rolled_prices, self.CFG["n"])
        upper_band = (ma_price + band_width).rename("upper_band")
        lower_band = (ma_price - band_width).rename("lower_band")

        indicator = pd.concat([self.prices, ma_price, upper_band, lower_band], axis=1)
        return indicator

    def signal(self, indicator: pd.DataFrame, continuous: bool, trend: bool):
        if continuous:
            signal = self._continuous_signal(indicator)
        else:
            signal = self._discreate_signal(indicator)
        if trend:
            signal["signal"] = signal["signal"] * -1
        return signal

    def _discreate_signal(self, indicator):
        signal = indicator.copy()
        signal["signal"] = 0.0

        over_band = signal["upper_band"] < signal["price"]
        under_band = signal["price"] < signal["lower_band"]

        signal.loc[over_band, "signal"] = -1.0
        signal.loc[under_band, "signal"] = 1.0
        return signal

    def _continuous_signal(self, indicator):
        signal = self._discreate_signal(indicator)

        over_band = signal["upper_band"] < signal["price"]
        under_band = signal["price"] < signal["lower_band"]
        in_band = ~(over_band | under_band)

        def _calc_in_band_signal(price, upper_band, lower_band):
            upper_dist = upper_band - price
            lower_dist = price - lower_band
            signal = (upper_dist - lower_dist) / (upper_dist + lower_dist)
            return signal

        in_band_indicator = signal.loc[in_band, :]
        signal.loc[in_band, "signal"] = in_band_indicator.apply(
            lambda x: _calc_in_band_signal(x["price"], x["upper_band"], x["lower_band"]), axis=1
        )
        return signal
