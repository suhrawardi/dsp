import math
import numpy as np
from sinusoid import Sinusoid

PI2 = math.pi * 2

class ComplexSinusoid(Sinusoid):
    def evaluate(self, ts):
        ts = np.asarray(ts)
        phases = PI2 * self.freq * ts + self.offset
        ys = self.amp * np.exp(1j * phases)
        return ys
