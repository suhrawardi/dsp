import scipy
import signals.spectrum_parent as spectrum_parent
import signals.sound_wave as sound_wave

class Dct(spectrum_parent.SpectrumParent):
    @property
    def amps(self):
        return self.hs

    def __add__(self, other):
        if other == 0:
            return self

        assert self.framerate == other.framerate
        hs = self.hs + other.hs
        return Dct(hs, self.fs, self.framerate)

    __radd__ = __add__

    def make_wave(self):
        N = len(self.hs)
        ys = scipy.fftpack.idct(self.hs, type=2) / 2 / N
        return sound_wave.SoundWave(ys, framerate=self.framerate)
