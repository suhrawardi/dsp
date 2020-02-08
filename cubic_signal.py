import numpy as np
from parabolic_signal import ParabolicSignal

class CubicSignal(ParabolicSignal):
    def evaluate(self, ts):
        ys = ParabolicSignal.evaluate(self, ts)
        ys = np.cumsum(ys)
        ys = normalize(unbias(ys), self.amp)
        return ys

def unbias(ys):
    return ys - ys.mean()

def normalize(ys, amp=1.0):
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)
