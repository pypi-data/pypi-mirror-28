import _hwcounter


class Timer:
    def __init__(self):
        self._t0 = None
        self.cycles = None

    def __enter__(self):
        self._t0 = _hwcounter.count()
        return self

    def __exit__(self, type, value, traceback):
        self.cycles = _hwcounter.count_end() - self._t0
