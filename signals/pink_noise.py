import signals.noise as noise
import signals.uncorrelated_uniform_noise as uncorrelated_uniform_noise

class PinkNoise(noise.Noise):
    def __init__(self, amp=1.0, beta=1.0):
        self.amp = amp
        self.beta = beta

    def make_wave(self, duration=1, start=0, framerate=11025):
        signal = uncorrelated_uniform_noise.UncorrelatedUniformNoise()
        wave = signal.make_wave(duration, start, framerate)
        spectrum = wave.make_spectrum()

        spectrum.pink_filter(beta=self.beta)

        wave2 = spectrum.make_wave()
        wave2.unbias()
        wave2.normalize(self.amp)
        return wave2
