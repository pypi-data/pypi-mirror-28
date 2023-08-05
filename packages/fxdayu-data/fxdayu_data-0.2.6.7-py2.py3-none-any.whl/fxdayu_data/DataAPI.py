# encoding:utf-8
import os
from fxdayu_data import config
from fxdayu_data.data_api.basic.info import BasicInfo

__all__ = ["init_config", "set_file", "candle", "factor", "get", "MarketIndex"]

FILE = config.get()


def exec_config_file():
    import os
    if os.path.isfile(FILE):
        exec(compile(open(FILE).read(), FILE, 'exec'), globals())
    else:
        raise IOError("Config file: '{}' does not exist.".format(FILE))


def init_config():
    exec_config_file()


def use(name):
    set_file(config.get(name))


def set_file(file_path):
    global FILE
    FILE = file_path
    init_config()


def candle(symbols, freq="D", fields=None, start=None, end=None, length=None, adjust=None):
    """

    :param symbols: str | tuple(str) | hashable array
    :param freq:  str
    :param fields: str | tuple(str) | hashable array
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param length: int
    :param adjust: str | None
    :return: pd.DataFrame or pd.Panel
    """
    pass


def factor(symbols, fields=None, start=None, end=None, length=None):
    """

    :param symbols: str | tuple(str) | hashable array
    :param fields: str | tuple(str) | hashable array
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param length: int
    :return: pd.DataFrame or pd.Panel
    """
    pass


def bonus(symbol, fields=None, start=None, end=None, length=None):
    """

    :param symbol: str
    :param fields: str | tuple(str) | hashable array
    :param start: datetime.datetime
    :param end: datetime.datetime
    :param length: int
    :return: pd.DataFrame
    """
    pass

info = BasicInfo()


def get(api, *args, **kwargs):
    return globals()[api](*args, **kwargs)


init_config()
