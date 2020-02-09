import numpy as np
import signals.base_signal as base_signal

class SilentSignal(base_signal.BaseSignal):
    def evaluate(self, ts):
        return np.zeros(len(ts))
