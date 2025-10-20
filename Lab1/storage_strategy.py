# storage_strategy.py
import pickle

class StorageStrategy:
    def save(self, data, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError

class PickleStorage(StorageStrategy):
    def save(self, data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)