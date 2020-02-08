import numpy as np
from signal import Signal

class UncorrelatedUniformNoise(_Noise):
    def evaluate(self, ts):
        ys = np.random.uniform(-self.amp, self.amp, len(ts))
        return ys
