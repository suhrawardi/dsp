import math
import numpy as np
import signals.base_signal as base_signal

PI2 = math.pi * 2

class Sinusoid(base_signal.BaseSignal):
    def __init__(self, freq=440, amp=1.0, offset=0, func=np.sin):
        self.freq = freq
        self.amp = amp
        self.offset = offset
        self.func = func

    @property
    def period(self):
        return 1.0 / self.freq

    def evaluate(self, ts):
        ts = np.asarray(ts)
        phases = PI2 * self.freq * ts + self.offset
        ys = self.amp * self.func(phases)
        return ys
