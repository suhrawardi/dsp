import numpy as np
import signals.noise as noise

class UncorrelatedUniformNoise(noise.Noise):
    def evaluate(self, ts):
        ys = np.random.uniform(-self.amp, self.amp, len(ts))
        return ys
