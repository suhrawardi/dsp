import math
import numpy as np
import signals.sinusoid as sinusoid

PI2 = math.pi * 2

class ComplexSinusoid(sinusoid.Sinusoid):
    def evaluate(self, ts):
        ts = np.asarray(ts)
        phases = PI2 * self.freq * ts + self.offset
        ys = self.amp * np.exp(1j * phases)
        return ys
