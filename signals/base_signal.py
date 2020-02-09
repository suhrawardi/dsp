import numpy as np
import signals.sound_wave as sound_wave

class BaseSignal:
    def __add__(self, other):
        if other == 0:
            return self
        return SumSignal(self, other)

    __radd__ = __add__

    @property
    def period(self):
        return 0.1

    def plot(self, framerate=11025):
        duration = self.period * 3
        wave = self.make_wave(duration, start=0, framerate=framerate)
        wave.plot()

    def make_wave(self, duration=1, start=0, framerate=11025):
        n = round(duration * framerate)
        ts = start + np.arange(n) / framerate
        ys = self.evaluate(ts)
        return sound_wave.SoundWave(ys, ts, framerate=framerate)


class SumSignal(BaseSignal):
    def __init__(self, *args):
        self.signals = args

    @property
    def period(self):
        return max(sig.period for sig in self.signals)

    def evaluate(self, ts):
        ts = np.asarray(ts)
        return sum(sig.evaluate(ts) for sig in self.signals)
