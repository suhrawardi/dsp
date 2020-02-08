import numpy as np
from noise import Noise

class UncorrelatedGaussianNoise(Noise):
    def evaluate(self, ts):
        ys = np.random.normal(0, self.amp, len(ts))
        return ys
