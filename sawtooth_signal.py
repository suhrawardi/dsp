import math
import numpy as np
from sinusoid import Sinusoid

PI2 = math.pi * 2

class SawtoothSignal(Sinusoid):
    def evaluate(self, ts):
        ts = np.asarray(ts)
        cycles = self.freq * ts + self.offset / PI2
        frac, _ = np.modf(cycles)
        ys = normalize(unbias(frac), self.amp)
        return ys

def unbias(ys):
    return ys - ys.mean()

def normalize(ys, amp=1.0):
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)
