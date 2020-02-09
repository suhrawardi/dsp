import signals.base_signal as base_signal

class Noise(base_signa.BaseSignal):
    def __init__(self, amp=1.0):
        self.amp = amp

    @property
    def period(self):
        return ValueError("Non-periodic signal.")
