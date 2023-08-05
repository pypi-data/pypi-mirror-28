from fxdayu_data.costume.basic import BasicTarget
import pandas as pd


class FileTarget(BasicTarget):

    def __init__(self, name):
        self.name = name
        self.index = "datetime"
        try:
            self._table = pd.read_csv(self.name, index_col=self.index)
        except IOError:
            self._table = pd.DataFrame(index=pd.Index(name=self.index))

    def flush(self):
        self._table.to_csv(self.name)

    def get(self, key):
        return self._table.loc[key]

    def set(self, key, value):
        self._table.loc[key] = value
        self._table.sort_index(inplace=True)
        self.flush()

    def inplace(self, frame):
        self._table = frame
        self.flush()

    def all(self):
        return self._table
