import numpy as np
from signals.sound_wave import SoundWave as Wave

class Spectrogram:
    def __init__(self, spec_map, seg_length):
        self.spec_map = spec_map
        self.seg_length = seg_length

    def any_spectrum(self):
        index = next(iter(self.spec_map))
        return self.spec_map[index]

    @property
    def time_res(self):
        spectrum = self.any_spectrum()
        return float(self.seg_length) / spectrum.framerate

    @property
    def freq_res(self):
        return self.any_spectrum().freq_res

    def times(self):
        ts = sorted(iter(self.spec_map))
        return ts

    def frequencies(self):
        fs = self.any_spectrum().fs
        return fs

    def plot(self, high=None, **options):
        fs = self.frequencies()
        i = None if high is None else find_index(high, fs)
        fs = fs[:i]
        ts = self.times()

        # make the array
        size = len(fs), len(ts)
        array = np.zeros(size, dtype=np.float)

        for j, t in enumerate(ts):
            spectrum = self.spec_map[t]
            array[:, j] = spectrum.amps[:i]

        thinkplot.pcolor(ts, fs, array, **options)

    def make_wave(self):
        res = []
        for t, spectrum in sorted(self.spec_map.items()):
            wave = spectrum.make_wave()
            n = len(wave)

            window = 1 / np.hamming(n)
            wave.window(window)

            i = wave.find_index(t)
            start = i - n // 2
            end = start + n
            res.append((start, end, wave))

        starts, ends, waves = zip(*res)
        low = min(starts)
        high = max(ends)

        ys = np.zeros(high - low, np.float)
        for start, end, wave in res:
            ys[start:end] = wave.ys

        # ts = np.arange(len(ys)) / self.framerate
        return Wave(ys, framerate=wave.framerate)

def find_index(x, xs):
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))
    return int(i)
