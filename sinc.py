import numpy as np
from sinusoid import Sinusoid

def Sinc(freq=440, amp=1.0, offset=0):
    return Sinusoid(freq, amp, offset, func=np.sinc)
