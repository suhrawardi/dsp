import numpy as np
import signals.base_signal as base_signal

class Impulses(base_signal.BaseSignal):
    def __init__(self, locations, amps=1):
        self.locations = np.asanyarray(locations)
        self.amps = amps

    def evaluate(self, ts):
        ys = np.zeros(len(ts))
        indices = np.searchsorted(ts, self.locations)
        ys[indices] = self.amps
        return ys
