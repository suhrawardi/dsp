import numpy as np
import signals.sinusoid as sinusoid

def Sinc(freq=440, amp=1.0, offset=0):
    return sinusoid.Sinusoid(freq, amp, offset, func=np.sinc)
