import pandas as pd
from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def indicator():
        pass

    @abstractmethod
    def signal(self, indicator: pd.DataFrame, continious: bool, trend: bool):
        if continious:
            signal = self._continuous_signal(indicator)
        else:
            signal = self._discreate_signal(indicator)
        if trend:
            signal["signal"] = signal["signal"] * -1
        return signal

    @abstractmethod
    def _continuous_signal():
        pass

    @abstractmethod
    def _discreate_signal():
        pass
