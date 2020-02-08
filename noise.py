from signal import Signal

class Noise(Signal):
    def __init__(self, amp=1.0):
        self.amp = amp

    @property
    def period(self):
        return ValueError("Non-periodic signal.")
