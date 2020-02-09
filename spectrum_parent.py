import copy
import numpy as np
import scipy

class SpectrumParent:
    def __init__(self, hs, fs, framerate, full=False):
        self.hs = np.asanyarray(hs)
        self.fs = np.asanyarray(fs)
        self.framerate = framerate
        self.full = full

    @property
    def max_freq(self):
        return self.framerate / 2

    @property
    def amps(self):
        return np.absolute(self.hs)

    @property
    def power(self):
        return self.amps ** 2

    def copy(self):
        return copy.deepcopy(self)

    def max_diff(self, other):
        assert self.framerate == other.framerate
        assert len(self) == len(other)

        hs = self.hs - other.hs
        return np.max(np.abs(hs))

    def ratio(self, denom, thresh=1, val=0):
        ratio_spectrum = self.copy()
        ratio_spectrum.hs /= denom.hs
        ratio_spectrum.hs[denom.amps < thresh] = val
        return ratio_spectrum

    def invert(self):
        inverse = self.copy()
        inverse.hs = 1 / inverse.hs
        return inverse

    @property
    def freq_res(self):
        return self.framerate / 2 / (len(self.fs) - 1)

    def render_full(self, high=None):
        hs = np.fft.fftshift(self.hs)
        amps = np.abs(hs)
        fs = np.fft.fftshift(self.fs)
        i = 0 if high is None else find_index(-high, fs)
        j = None if high is None else find_index(high, fs) + 1
        return fs[i:j], amps[i:j]

    def plot(self, high=None, **options):
        if self.full:
            fs, amps = self.render_full(high)
            thinkplot.plot(fs, amps, **options)
        else:
            i = None if high is None else find_index(high, self.fs)
            thinkplot.plot(self.fs[:i], self.amps[:i], **options)

    def plot_power(self, high=None, **options):
        if self.full:
            fs, amps = self.render_full(high)
            thinkplot.plot(fs, amps ** 2, **options)
        else:
            i = None if high is None else find_index(high, self.fs)
            thinkplot.plot(self.fs[:i], self.power[:i], **options)

    def estimate_slope(self):
        x = np.log(self.fs[1:])
        y = np.log(self.power[1:])
        t = scipy.stats.linregress(x, y)
        return t

    def peaks(self):
        t = list(zip(self.amps, self.fs))
        t.sort(reverse=True)
        return t

def find_index(x, xs):
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))
    return int(i)
