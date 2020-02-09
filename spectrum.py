import numpy as np
from signals.spectrum_parent import SpectrumParent
from signals.sound_wave import SoundWave as Wave

class Spectrum(SpectrumParent):
    def __len__(self):
        return len(self.hs)

    def __add__(self, other):
        if other == 0:
            return self.copy()

        assert all(self.fs == other.fs)
        hs = self.hs + other.hs
        return Spectrum(hs, self.fs, self.framerate, self.full)

    __radd__ = __add__

    def __mul__(self, other):
        assert all(self.fs == other.fs)
        hs = self.hs * other.hs
        return Spectrum(hs, self.fs, self.framerate, self.full)

    def convolve(self, other):
        assert all(self.fs == other.fs)
        if self.full:
            hs1 = np.fft.fftshift(self.hs)
            hs2 = np.fft.fftshift(other.hs)
            hs = np.convolve(hs1, hs2, mode="same")
            hs = np.fft.ifftshift(hs)
        else:
            # not sure this branch would mean very much
            hs = np.convolve(self.hs, other.hs, mode="same")

        return Spectrum(hs, self.fs, self.framerate, self.full)

    @property
    def real(self):
        return np.real(self.hs)

    @property
    def imag(self):
        return np.imag(self.hs)

    @property
    def angles(self):
        return np.angle(self.hs)

    def scale(self, factor):
        self.hs *= factor

    def low_pass(self, cutoff, factor=0):
        self.hs[abs(self.fs) > cutoff] *= factor

    def high_pass(self, cutoff, factor=0):
        self.hs[abs(self.fs) < cutoff] *= factor

    def band_stop(self, low_cutoff, high_cutoff, factor=0):
        fs = abs(self.fs)
        indices = (low_cutoff < fs) & (fs < high_cutoff)
        self.hs[indices] *= factor

    def pink_filter(self, beta=1):
        denom = self.fs ** (beta / 2.0)
        denom[0] = 1
        self.hs /= denom

    def differentiate(self):
        new = self.copy()
        new.hs *= PI2 * 1j * new.fs
        return new

    def integrate(self):
        new = self.copy()
        new.hs /= PI2 * 1j * new.fs
        return new

    def make_integrated_spectrum(self):
        cs = np.cumsum(self.power)
        cs /= cs[-1]
        return IntegratedSpectrum(cs, self.fs)

    def make_wave(self):
        if self.full:
            ys = np.fft.ifft(self.hs)
        else:
            ys = np.fft.irfft(self.hs)

        return Wave(ys, framerate=self.framerate)
