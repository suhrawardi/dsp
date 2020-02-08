import math
import numpy as np
from sinusoid import Sinusoid

PI2 = math.pi * 2

class SquareSignal(Sinusoid):
    def evaluate(self, ts):
        ts = np.asarray(ts)
        cycles = self.freq * ts + self.offset / PI2
        frac, _ = np.modf(cycles)
        ys = self.amp * np.sign(unbias(frac))
        return ys

def unbias(ys):
    return ys - ys.mean()
