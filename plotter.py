import pandas as pd
from pylab import plt, mpl

class Plotter:
    def __init__(self, name, xs, ys):
        self.name = name
        self.xs = xs
        self.ys = ys

        plt.style.use('seaborn')
        mpl.rcParams['font.family'] = 'serif'

    def plot(self):
        df = pd.DataFrame(self.xs, index=self.ys)
        ax = df.plot(lw=2.0, figsize=(10, 6))
        ax.figure.savefig("plots/" + self.name + ".pdf")
