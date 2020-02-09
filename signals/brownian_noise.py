import signals.noise as noise
import numpy as np

class BrownianNoise(noise.Noise):
    def evaluate(self, ts):
        dys = np.random.uniform(-1, 1, len(ts))
        # ys = scipy.integrate.cumtrapz(dys, ts)
        ys = np.cumsum(dys)
        ys = normalize(unbias(ys), self.amp)
        return ys
