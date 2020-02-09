import numpy as np
import signals.noise as noise

class UncorrelatedGaussianNoise(noise.Noise):
    def evaluate(self, ts):
        ys = np.random.normal(0, self.amp, len(ts))
        return ys
