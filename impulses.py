import numpy as np
from signal import Signal

class Impulses(Signal):
    def __init__(self, locations, amps=1):
        self.locations = np.asanyarray(locations)
        self.amps = amps

    def evaluate(self, ts):
        ys = np.zeros(len(ts))
        indices = np.searchsorted(ts, self.locations)
        ys[indices] = self.amps
        return ys
