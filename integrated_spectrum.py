import numpy as np
import thinkplot

class IntegratedSpectrum:
    def __init__(self, cs, fs):
        self.cs = np.asanyarray(cs)
        self.fs = np.asanyarray(fs)

    def plot_power(self, low=0, high=None, expo=False, **options):
        cs = self.cs[low:high]
        fs = self.fs[low:high]

        if expo:
            cs = np.exp(cs)

        thinkplot.plot(fs, cs, **options)

    def estimate_slope(self, low=1, high=-12000):
        # print self.fs[low:high]
        # print self.cs[low:high]
        x = np.log(self.fs[low:high])
        y = np.log(self.cs[low:high])
        t = scipy.stats.linregress(x, y)
        return t
