import copy
import numpy as np
import subprocess
import warnings
import plotter

class SoundWave:
    def __init__(self, ys, ts=None, framerate=None):
        self.ys = np.asanyarray(ys)
        self.framerate = framerate if framerate is not None else 11025

        if ts is None:
            self.ts = np.arange(len(ys)) / self.framerate
        else:
            self.ts = np.asanyarray(ts)

    def copy(self):
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.ys)

    @property
    def start(self):
        return self.ts[0]

    @property
    def end(self):
        return self.ts[-1]

    @property
    def duration(self):
        return len(self.ys) / self.framerate

    def __add__(self, other):
        if other == 0:
            return self

        assert self.framerate == other.framerate

        # make an array of times that covers both waves
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        n = int(round((end - start) * self.framerate)) + 1
        ys = np.zeros(n)
        ts = start + np.arange(n) / self.framerate

        def add_ys(wave):
            i = find_index(wave.start, ts)

            # make sure the arrays line up reasonably well
            diff = ts[i] - wave.start
            dt = 1 / wave.framerate
            if (diff / dt) > 0.1:
                warnings.warn(
                    "Can't add these waveforms; their " "time arrays don't line up."
                )

            j = i + len(wave)
            ys[i:j] += wave.ys

        add_ys(self)
        add_ys(other)

        return SoundWave(ys, ts, self.framerate)

    __radd__ = __add__

    def __or__(self, other):
        if self.framerate != other.framerate:
            raise ValueError("Wave.__or__: framerates do not agree")

        ys = np.concatenate((self.ys, other.ys))
        # ts = np.arange(len(ys)) / self.framerate
        return SoundWave(ys, framerate=self.framerate)

    def __mul__(self, other):
        # the spectrums have to have the same framerate and duration
        assert self.framerate == other.framerate
        assert len(self) == len(other)

        ys = self.ys * other.ys
        return SoundWave(ys, self.ts, self.framerate)

    def max_diff(self, other):
        assert self.framerate == other.framerate
        assert len(self) == len(other)

        ys = self.ys - other.ys
        return np.max(np.abs(ys))

    def convolve(self, other):
        if isinstance(other, Wave):
            assert self.framerate == other.framerate
            window = other.ys
        else:
            window = other

        ys = np.convolve(self.ys, window, mode="full")
        # ts = np.arange(len(ys)) / self.framerate
        return SoundWave(ys, framerate=self.framerate)

    def diff(self):
        ys = np.diff(self.ys)
        ts = self.ts[1:].copy()
        return SoundWave(ys, ts, self.framerate)

    def cumsum(self):
        ys = np.cumsum(self.ys)
        ts = self.ts.copy()
        return SoundWave(ys, ts, self.framerate)

    def quantize(self, bound, dtype):
        return quantize(self.ys, bound, dtype)

    def apodize(self, denom=20, duration=0.1):
        self.ys = apodize(self.ys, self.framerate, denom, duration)

    def hamming(self):
        self.ys *= np.hamming(len(self.ys))

    def window(self, window):
        self.ys *= window

    def scale(self, factor):
        self.ys *= factor

    def shift(self, shift):
        # TODO: track down other uses of this function and check them
        self.ts += shift

    def roll(self, roll):
        self.ys = np.roll(self.ys, roll)

    def truncate(self, n):
        self.ys = truncate(self.ys, n)
        self.ts = truncate(self.ts, n)

    def zero_pad(self, n):
        self.ys = zero_pad(self.ys, n)
        self.ts = self.start + np.arange(n) / self.framerate

    def normalize(self, amp=1.0):
        self.ys = normalize(self.ys, amp=amp)

    def unbias(self):
        self.ys = unbias(self.ys)

    def find_index(self, t):
        n = len(self)
        start = self.start
        end = self.end
        i = round((n - 1) * (t - start) / (end - start))
        return int(i)

    def segment(self, start=None, duration=None):
        if start is None:
            start = self.ts[0]
            i = 0
        else:
            i = self.find_index(start)

        j = None if duration is None else self.find_index(start + duration)
        return self.slice(i, j)

    def slice(self, i, j):
        ys = self.ys[i:j].copy()
        ts = self.ts[i:j].copy()
        return SoundWave(ys, ts, self.framerate)

    def make_spectrum(self, full=False):
        n = len(self.ys)
        d = 1 / self.framerate

        if full:
            hs = np.fft.fft(self.ys)
            fs = np.fft.fftfreq(n, d)
        else:
            hs = np.fft.rfft(self.ys)
            fs = np.fft.rfftfreq(n, d)

        return Spectrum(hs, fs, self.framerate, full)

    def make_dct(self):
        N = len(self.ys)
        hs = scipy.fftpack.dct(self.ys, type=2)
        fs = (0.5 + np.arange(N)) / 2
        return Dct(hs, fs, self.framerate)

    def make_spectrogram(self, seg_length, win_flag=True):
        if win_flag:
            window = np.hamming(seg_length)
        i, j = 0, seg_length
        step = int(seg_length // 2)

        # map from time to Spectrum
        spec_map = {}

        while j < len(self.ys):
            segment = self.slice(i, j)
            if win_flag:
                segment.window(window)

            # the nominal time for this segment is the midpoint
            t = (segment.start + segment.end) / 2
            spec_map[t] = segment.make_spectrum()

            i += step
            j += step

        return Spectrogram(spec_map, seg_length)

    def get_xfactor(self, options):
        try:
            xfactor = options["xfactor"]
            options.pop("xfactor")
        except KeyError:
            xfactor = 1
        return xfactor

    def plot(self, name="sound", **options):
        xfactor = self.get_xfactor(options)
        print("Plotting " + name)
        p = plotter.Plotter(name, self.ys, self.ts * xfactor)
        p.plot()

    def corr(self, other):
        corr = np.corrcoef(self.ys, other.ys)[0, 1]
        return corr

    def cov_mat(self, other):
        return np.cov(self.ys, other.ys)

    def cov(self, other):
        total = sum(self.ys * other.ys) / len(self.ys)
        return total

    def cos_cov(self, k):
        n = len(self.ys)
        factor = math.pi * k / n
        ys = [math.cos(factor * (i + 0.5)) for i in range(n)]
        total = 2 * sum(self.ys * ys)
        return total

    def cos_transform(self):
        n = len(self.ys)
        res = []
        for k in range(n):
            cov = self.cos_cov(k)
            res.append((k, cov))

        return res

    def write(self, filename="sound"):
        print("Writing " + filename + ".wav")
        wfile = WavFileWriter(filename, self.framerate)
        wfile.write(self)
        wfile.close()


def normalize(ys, amp=1.0):
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)

def apodize(ys, framerate, denom=20, duration=0.1):
    # a fixed fraction of the segment
    n = len(ys)
    k1 = n // denom

    # a fixed duration of time
    k2 = int(duration * framerate)

    k = min(k1, k2)

    w1 = np.linspace(0, 1, k)
    w2 = np.ones(n - 2 * k)
    w3 = np.linspace(1, 0, k)

    window = np.concatenate((w1, w2, w3))
    return ys * window

def find_index(x, xs):
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))
    return int(i)

def quantize(ys, bound, dtype):
    if max(ys) > 1 or min(ys) < -1:
        warnings.warn("Warning: normalizing before quantizing.")
        ys = normalize(ys)

    zs = (ys * bound).astype(dtype)
    return zs

def unbias(ys):
    return ys - ys.mean()
