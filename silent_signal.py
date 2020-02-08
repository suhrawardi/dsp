import numpy as np
from signal import Signal

class SilentSignal(Signal):

    def evaluate(self, ts):
        return np.zeros(len(ts))
