from fxdayu_data.data_api import lru_cache
from fxdayu_data.data_api.basic.candle import BasicCandle, normalize
from fxdayu_data.data_api.bundle.blp_reader import DateCandleTable, DateAdjustTable, FactorReader
import pandas as pd


class BLPCandle(BasicCandle):

    def __init__(self):
        self.tables = {}
        self.adjust = None

    def __call__(self, symbols, freq, fields=None, start=None, end=None, length=None, adjust=None):
        return self.read(
            *normalize(symbols, freq, fields, start, end, length, adjust)
        )

    @lru_cache(maxsize=256)
    def read(self, symbols, freq, fields=None, start=None, end=None, length=None, adjust=None):
        candle = self.tables[freq].read(symbols, fields, start, end, length)
        if adjust is None:
            return candle
        else:
            if isinstance(candle, pd.DataFrame):
                adjust = self.get_adjust(symbols, candle.index[0], candle.index[-1], adjust)
                return adjust_candle(candle, adjust)
            elif isinstance(candle, pd.Panel):
                return pd.Panel.from_dict(
                    {symbol: adjust_candle(frame, self.get_adjust(symbol, frame.index[0], frame.index[-1], adjust))
                     for symbol, frame in candle.items()}
                )

    def find(self, name, freq="D"):
        return self.tables[freq].find(name)

    def set(self, **kwargs):
        for freq, rootdir in list(kwargs.items()):
            self.tables[freq] = DateCandleTable(rootdir)

    def set_adjust(self, rootdir):
        self.adjust = DateAdjustTable(rootdir)

    def get_adjust(self, name, start, end, type):
        adjust = self.adjust.read(name, start, end)
        if type == 'after':
            return adjust
        else:
            return adjust/adjust.iloc[-1]


PRICE = ("open", "high", "low", "close")


def adjust_candle(frame, adjust_factor):
    factor = pd.Series(adjust_factor, frame.index).bfill()
    for name in frame.columns:
        if name in PRICE:
            frame[name] = frame[name] * factor
    return frame


class BLPFactor(BasicConfig):

    def __init__(self, path):
        self.reader = FactorReader(path)

    @lru_cache(maxsize=256)
    def __call__(self, symbols, fields=None, start=None, end=None, length=None):
        return self.reader.read(symbols, fields, start, end, length)

    def find(self, name):
        return self.reader.find(name)
